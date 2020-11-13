#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, re, os

from tweak_program_helpers import make_parser, do_loop, get_cmssw_version, isCMSSWSupported

def handle_dqmSaver(process, args):

   if not hasattr(process,'dqmSaver'):
      return process

   setattr(process.dqmSaver,"runIsComplete",cms.untracked.bool(args.runIsComplete))
   if args.multiRun and isCMSSWSupported(get_cmssw_version(), "CMSSW_8_0_0"):
      setattr(process.dqmSaver,"forceRunNumber",cms.untracked.int32(999999))

   if args.datasetName:
      if args.multiRun:
         datasetName = args.datasetName.rsplit('/', 1)
         datasetName[0] += args.runLimits
         datasetName = "/".join(datasetName)
      setattr(process.dqmSaver,"workflow", cms.untracked.string(datasetName))
   return process

def init_argparse():
    parser = make_parser("Enable the lazy download service")
    parser.add_argument('--runIsComplete', action='store_true', required=False)
    parser.add_argument('--multiRun', action='store_true', required=False)
    parser.add_argument('--runLimits', default="", required=False)
    parser.add_argument('--datasetName', default=None, required=False)

    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    do_loop(args, handle_dqmSaver)

main()
