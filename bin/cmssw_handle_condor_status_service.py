#!/bin/sh 

""":"

python_cmd="python"
python3 -c "from FWCore.PythonFramework.CmsRun import CmsRun" 2>/dev/null && python_cmd="python3"
exec ${python_cmd} $0 ${1+"$@"}

"""

import sys, os
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '..', 'python'))

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import re

from tweak_program_helpers import make_parser, do_loop, get_cmssw_version, isCMSSWSupported



def handle_condor(process, args):
   name = args.name

   if isCMSSWSupported(get_cmssw_version(), "CMSSW_7_6_0"):
      process.add_(cms.Service("CondorStatusService", tag=cms.untracked.string("_%s_" % name)))
      print("Added CondorStatusService")
   else:
      print("CondorStatusService is not supported")
   return process

def init_argparse():
    parser = make_parser("Handle random number seeding")
    parser.add_argument('--name', required=True)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    do_loop(args, handle_condor)

main()
