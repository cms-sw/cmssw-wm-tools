#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, re, os

from tweak_program_helpers import make_parser, do_loop, get_cmssw_version, isCMSSWSupported



def handle_seeds(process, args):
   name = args.name[0]

   if isCMSSWSupported(get_cmssw_version(), "CMSSW_7_6_0"):
      process.add_(cms.Service("CondorStatusService", tag=cms.untracked.string("_%s_" % name)))
      
   return process

def init_argparse():
    parser = make_parser("Handle random number seeding")
    parser.add_argument('--name', nargs='+', required=True)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    do_loop(args, handle_seeds)

main()
