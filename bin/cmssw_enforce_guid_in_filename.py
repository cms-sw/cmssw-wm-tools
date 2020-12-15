#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, os

from tweak_program_helpers import make_parser, do_loop, get_cmssw_version, adjust_source_guid 
from tweak_program_helpers import isCMSSWSupported

def adjust_guid(process, args):

    input_source_names = args.input_source
    for input_source_name in input_source_names:
       input_source = process
       name_sp = input_source_name.split('.')
       if name_sp[0] == "process" and len(name_sp) > 1: 
          name_sp = name_sp[1:]
       for key in name_sp:
          input_source = getattr(input_source,key)
       adjust_source_guid(input_source)
       
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
