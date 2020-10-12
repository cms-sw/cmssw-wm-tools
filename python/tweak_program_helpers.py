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
