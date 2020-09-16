#!/usr/bin/env python

import pickle
try: 
   import argparse
except ImportError: #get it from this package instead
   import archived_argparse as argparse 
import sys


def param_value(process, key):
    key_split = key.split('.')
    param = process
    if key_split[0] == "process":
        key_split = key_split[1:]
    for p in key_split:
        if hasattr(param,p):
           param = getattr(param, p)
        else:
           return None
    return param

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Print out param value(s) from pset(s)"
    )
    parser.add_argument('--param', nargs='+', required=True)
    parser.add_argument('--input_pkl', nargs='+', required=True)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    for i in range(len(args.input_pkl)):
        with open(args.input_pkl[i], "rb") as pkl_file:
            try:
                process = pickle.load(pkl_file)
            except (IOError, OSError, pickle.PickleError, pickle.UnpicklingError):
                print("Not a valid pickle file " +
                      args.input_pkl[i]) + "- stopping"
                sys.exit(1)
        print(args.input_pkl[i]) 
        for param in args.param:
           print("   "+param+" is "+str(param_value(process,param)))

main()

