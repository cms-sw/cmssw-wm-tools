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



def custom_timeout(process, args):

   # XrdAdaptor uses 3*60 unless non-zero value is specified here
   timeout = args.timeout
   if hasattr(process, "SiteLocalConfigService"):
      process.SiteLocalConfigService.overrideSourceTimeout = cms.untracked.uint32(timeout)
   else:
      process.add_(cms.Service("SiteLocalConfigService",
                               overrideSourceTimeout = cms.untracked.uint32(timeout)))
   
   return process

def init_argparse():
    parser = make_parser("Enable custom timeout service")
    parser.add_argument('--timeout', type=int, default=600, required=False)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    do_loop(args, custom_timeout)

main()
