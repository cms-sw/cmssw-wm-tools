#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, os



def make_parser(help_string):
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description=help_string
    )
    parser.add_argument('--input_pkl', nargs='+', required=True)
    parser.add_argument('--output_pkl', nargs='+', required=False)
    return parser


def do_loop(args,func):
   if len(args.output_pkl) != 0:
        output_file_names = args.output_pkl
        if len(args.input_pkl) != len(args.output_pkl):
            print(
                "Incorrect arguments. --input_pkl and --output_pkl must be the same length")
            sys.exit(1)
   else:
       output_file_names=args.input_pkl

   for i in range(len(args.input_pkl)):
        with open(args.input_pkl[i], "rb") as pkl_file:
            try:
                process = pickle.load(pkl_file)
            except (IOError, OSError, pickle.PickleError, pickle.UnpicklingError):
                print("Not a valid pickle file " +
                      args.input_pkl[i]) + "- stopping"
                sys.exit(1)

        # do stuff here.
        process = func(process, args)

        with open(output_file_names[i], "wb") as output_file:
            if output_file.closed:
                print("Error loading pickle input "+args.output_pkl[i])
                sys.exit(1)
            pickle.dump(process, output_file, protocol=0)


def get_cmssw_version():
    return os.environ["CMSSW_VERSION"]


def isCMSSWSupported(thisCMSSW, supportedCMSSW):
    """
    _isCMSSWSupported_
    Function used to validate whether the CMSSW release to be used supports
    a feature that is not available in all releases.
    :param thisCMSSW: release to be used in this job
    :param allowedCMSSW: first (lowest) release that started supporting the
    feature you'd like to use.
    
    NOTE: only the 3 digits version are evaluated, pre and patch releases
    are not taken into consideration
    """
    if not thisCMSSW or not supportedCMSSW:
        return False

    if thisCMSSW == supportedCMSSW:
        return True

    thisCMSSW = [int(i) for i in thisCMSSW.split('_', 4)[1:4]]
    supportedCMSSW = [int(i) for i in supportedCMSSW.split('_', 4)[1:4]]
    for idx in range(3):
        if thisCMSSW[idx] > supportedCMSSW[idx]:
            return True
        elif thisCMSSW[idx] == supportedCMSSW[idx] and idx < 2:
            if thisCMSSW[idx + 1] > supportedCMSSW[idx + 1]:
                return True
        else:
            return False

    return False

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

def adjust_source_guid(input_source):
   import re
   guidRegEx = re.compile("[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}.root$")
   current_cmssw = get_cmssw_version()

   if not isEnforceGUIDInFileNameSupported(current_cmssw):
      print("GUID enforcement not supported in this CMSSW release ("+current_cmssw+")")
      return 
   print("GUID in this CMSSW release ("+current_cmssw+") is supported")
   print("Considering a source of type "+input_source.type_())
   if input_source.type_() not in ["PoolSource", "EmbeddedRootSource"]:
      return
   if not guidRegEx.search(input_source.fileNames[0]):
      return
   input_source.enforceGUIDInFileName = cms.untracked.bool(True)
   print("Enabled GUID enforcement for a "+input_source.type_())
   return
