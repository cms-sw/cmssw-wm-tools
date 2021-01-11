#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, re, os


def init_argparse():
   parser = argparse.ArgumentParser(
      usage="%(prog)s [OPTION] [FILE]...",
      description="Pickle a pset file"
   )
   
   parser.add_argument('--input', required=True)
   parser.add_argument('--output_pkl', required=True)
   return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()

    with open(args.input) as f:
        code = compile(f.read(), args.input, 'exec')
        exec(code, globals(), locals())

    with open(args.output_pkl, "wb") as pHandle:
        pickle.dump(process, pHandle)

main()
