#!/bin/sh 

""":"

python_cmd="python"
python3 -c "from FWCore.PythonFramework.CmsRun import CmsRun" 2>/dev/null && python_cmd="python3"
exec ${python_cmd} $0 ${1+"$@"}

"""

import FWCore.ParameterSet.Config as cms
import pickle
try:
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse
import sys, re, os

# Use the same default protocol as in python 2.
pickle.DEFAULT_PROTOCOL = 0

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
    globals={}
    locals={}

    with open(args.input) as f:
        code = compile(f.read(), args.input, 'exec')
        exec(code, globals, locals)

    with open(args.output_pkl, "wb") as pHandle:
        pickle.dump(locals['process'], pHandle, protocol=pickle.DEFAULT_PROTOCOL)

main()
