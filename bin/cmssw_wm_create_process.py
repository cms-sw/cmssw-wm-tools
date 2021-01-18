#!/usr/bin/env python

import sys, os
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '..', 'python'))

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import re, os
import json

from tweak_program_helpers import make_parser



def create_process(args,func_args):

   
   if args.funcname == "merge":
      if not args.useErrorDataset:
         func_args['outputmod_label'] = "MergedError"
         
      try:
         from Configuration.DataProcessing.Merge import mergeProcess
         process = mergeProcess(**func_args)
      except Exception as ex:
         msg = "Failed to create a merge process."
         print(msg)
         raise ex
   elif args.funcname == "repack":
      try:
         from Configuration.DataProcessing.Repack import repackProcess
         process = repackProcess(**func_args)
      except Exception as ex:
         msg = "Failed to create a repack process."
         print(msg)
         raise ex
   else:
      try:
         from Configuration.DataProcessing.GetScenario import getScenario
         scenarioInst = getScenario(scenario)
      except Exception as ex:
         msg = "Failed to retrieve the Scenario named "
         msg += str(scenario)
         msg += "\nWith Error:"
         msg += str(ex)
         print(msg)
         raise ex
      try:
         process = getattr(scenarioInst, args.funcname)(**func_args)
      except Exception as ex:
         msg = "Failed to load process from Scenario %s (%s)." % (scenario, scenarioInst)
         print(msg)
         raise ex
      
   return process

def init_argparse():
   parser = argparse.ArgumentParser(
      usage="%(prog)s [OPTION] [FILE]...",
      description="Process creator (merge, DataProcessing etc)"
   )
   
   parser.add_argument('--funcname', required=True)
   parser.add_argument('--funcargs', required=True)
   parser.add_argument('--useErrorDataset', action="store_true", required=False)
   parser.add_argument('--output_pkl', required=True)
   return parser


def main():
   parser = init_argparse()
   args = parser.parse_args()
   
   func_args={}
   
   try:
      with open(args.funcargs) as json_file:
         json_data = json.load(json_file)
   except Exception as e:
      print("Error opening file "+args.funcargs)
      sys.exit(1)
         
   if not isinstance(json_data,dict):
      print("Error loading dictionary "+args.funcargs)
      sys.exit(1)

   func_args = json_data

   process=create_process(args, func_args)

   with open(args.output_pkl, "wb") as output_file:
      if output_file.closed:
         print("Error loading pickle input "+args.output_pkl[i])
         sys.exit(1)
      pickle.dump(process, output_file, protocol=0)
         

main()
