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

def get_source_type(process):
    inputSource = getattr(process, "source", None)
    if inputSource is None:
        return None
    if hasattr(inputSource, "type_"):
        return inputSource.type_()
    if hasattr(inputSource, "_TypedParameterizable__type"):
        return inputSource._TypedParameterizable__type
    return None

def handle_lazy(process, args):
    if getattr(args, "check_lhe_workflow", False):
        source_type = get_source_type(process)
        if source_type != "LHESource":
            return process
    
    process.add_(cms.Service("SiteLocalConfigService",
                             overrideSourceCacheHintDir=cms.untracked.string("lazy-download")))
    print("Added lazy-download to SIteLocalConfigService")
    return process

def init_argparse():
    parser = make_parser("Enable the lazy download service")
    parser.add_argument("--check_lhe_workflow", action="store_true",
                         help="For LHE workflow, only enable lazy-download if process.source is LHESource")
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    do_loop(args, handle_lazy)

main()
