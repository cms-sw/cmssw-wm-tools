#!/usr/bin/env python

import sys, os
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '..', 'python'))

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import re, random

from tweak_program_helpers import make_parser, do_loop, get_cmssw_version 
from tweak_program_helpers import isCMSSWSupported, adjust_source_guid

def getPileupMixingModules(process):
   """
   Method returns two lists:
   1) list of mixing modules ("MixingModule")
   2) list of data mixing modules ("DataMixingModules")
   The first gets added only pileup files of type "mc", the
   second pileup files of type "data".
   """
   mixModules, dataMixModules = [], []
   prodsAndFilters = {}
   prodsAndFilters.update(process.producers)
   prodsAndFilters.update(process.filters)
   for key, value in prodsAndFilters.items():
      if value.type_() in ["MixingModule", "DataMixingModule", "PreMixingModule"]:
         mixModules.append(value)
      if value.type_() == "DataMixingModule":
         dataMixModules.append(value)
   return mixModules, dataMixModules

def read_json(f):
   import json
   try:
      with open(f) as json_file:
         json_data = json.load(json_file)
   except Exception as e:
      print("Error opening file "+f)
      sys.exit(1)
         
   if not isinstance(json_data,dict):
      print("Error loading dictionary "+f)
      sys.exit(1)

   return json_data


def process_pileup_mixing_modules(process, args, modules, requestedPileupType):
# this needs to be read from json
   pileupDict = read_json(args.pileup_dict)
   for m in modules:
      print("Processing " + m.type_() + " " + m.label_() + " type " + requestedPileupType)
      for pileupType in pileupDict.keys():
         # there should be either "input" or "secsource" attributes
         # and both "MixingModule", "DataMixingModule" can have both
         inputTypeAttrib = getattr(m, "input", None) or getattr(m, "secsource", None)
         if not inputTypeAttrib:
            continue
         inputTypeAttrib.fileNames = cms.untracked.vstring()
         if pileupType == requestedPileupType:
            eventsAvailable = pileupDict[pileupType]["eventsAvailable"]
            print("    Found "+str(eventsAvailable)+" events")
            for fileLFN in pileupDict[pileupType]["FileList"]:
               # vstring does not support unicode
               inputTypeAttrib.fileNames.append(str(fileLFN))
            print("    Added %4d files"%len(pileupDict[pileupType]["FileList"]))
            if requestedPileupType == 'data':
               if args.skip_pileup_events: 
                  # For deterministic pileup, we want to shuffle the list the
                  # same for every job in the task and skip events
                  random.seed(int(args.random_seed))
                  inputTypeAttrib.skipEvents = cms.untracked.uint32(
                     int(args.skip_pileup_events) % eventsAvailable)
                  inputTypeAttrib.sequential = cms.untracked.bool(True)
            # Shuffle according to the seed above or randomly
            random.shuffle(inputTypeAttrib.fileNames)
            
            # Handle enforceGUIDInFileName for pileup
            #DL: need to figure this one out..
            adjust_source_guid(inputTypeAttrib)
   return process            

def handle_pileup(process, args):
   mixModules, dataMixModules = getPileupMixingModules(process)
   process = process_pileup_mixing_modules(process, args, dataMixModules, "data")
   process = process_pileup_mixing_modules(process, args, mixModules, "mc")
   return process

def init_argparse():
    parser = make_parser("Handle random number seeding")
    parser.add_argument('--skip_pileup_events', required=False)
    parser.add_argument('--random_seed', required=False)
    parser.add_argument('--pileup_dict', required=True)
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    do_loop(args, handle_pileup)

main()
