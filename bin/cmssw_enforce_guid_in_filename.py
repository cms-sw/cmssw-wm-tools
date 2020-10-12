#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, re, os

from tweak_program_helpers import make_parser, do_loop, get_cmssw_version, isCMSSWSupported


def isEnforceGUIDInFileNameSupported(thisCMSSW):
    """
    _isEnforceGUIDInFileNameSupported_
    Function used to validate whether the CMSSW release to be used supports
    the enforceGUIDInFileName feature.
    :param thisCMSSW: release to be used in this job
    """
    # a set of CMSSW releases that support the enforceGUIDInFileName feature. Releases in the same
    # cycle with a higher minor revision number also support the feature.
    supportedReleases = set(["CMSSW_10_6_8", "CMSSW_10_2_20", "CMSSW_9_4_16", "CMSSW_9_3_17", "CMSSW_8_0_34"])
    # a set of specific CMSSW releases that supported the enforceGUIDInFileName feature.
    specificSupportedReleases = set(["CMSSW_10_2_20_UL", "CMSSW_9_4_16_UL", "CMSSW_8_0_34_UL", "CMSSW_7_1_45_patch3"])

    # true if CMSSW release is >= CMSSW_11_0_0
    if isCMSSWSupported(thisCMSSW, "CMSSW_11_0_0"):
        return True
    # true if CMSSW release is in the specific release set
    elif thisCMSSW in specificSupportedReleases:
        return True
    # true if the CMSSW release's minor revision is >= to one of the supported releases
    else:
        thisMajor, thisMid, thisMinor = [int(i) for i in thisCMSSW.split('_', 4)[1:4]]
        for release in supportedReleases:
            supportedMajor, supportedMid, supportedMinor = [int(i) for i in release.split('_', 4)[1:4]]
            # major and mid revisions need an exact match
            if thisMajor == supportedMajor and thisMid == supportedMid:
                # minor revision need to be >= to the supported minor revision
                if thisMinor >= supportedMinor:
                    return True
    return False


def adjust_guid(process, args):
    current_cmssw = get_cmssw_version()

    if not isEnforceGUIDInFileNameSupported(current_cmssw):
        return process

    input_source_names = args.input_source
    guidRegEx = re.compile("[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}.root$")

    for input_source_name in input_source_names:
       input_source = process
       name_sp = input_source_name.split('.')
       if name_sp[0] == "process" and len(name_sp) > 1: 
          name_sp = name_sp[1:]
       for key in name_sp:
          input_source = getattr(input_source,key)

       if input_source.type_() not in ["PoolSource", "EmbeddedRootSource"]:
         continue
       print input_source
       if not guidRegEx.search(input_source.fileNames[0]):
          continue
       input_source.enforceGUIDInFileName = cms.untracked.bool(True)
        
    return process

def init_argparse():
    parser = make_parser("Add GUID enforcement support")
    parser.add_argument('--input_source', nargs='+', required=True)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    do_loop(args, adjust_guid)

main()
