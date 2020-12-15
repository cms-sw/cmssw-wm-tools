#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, re, os

from tweak_program_helpers import make_parser, do_loop

def handle_nEvents(process, args):
   
   for producer in process.producers:
      if hasattr(getattr(process, producer), "nEvents"):
         getattr(process, producer).nEvents = process.maxEvents.input.value()

   return process

def init_argparse():
    parser = make_parser("Set nEvents appropriately in producers")
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    do_loop(args, handle_nEvents)

main()
