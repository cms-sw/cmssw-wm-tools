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

    seedings = args.seeding

    if not hasattr(process, "RandomNumberGeneratorService"):
       return process

    for seeding in seedings:
       if seeding == "ReproducibleSeeding":
          randService = process.RandomNumberGeneratorService
          for x in randService:
             getattr(process.RandomNumberGeneratorService,x._internal_name).initialSeed = x.initialSeed
       else:
          from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
          helper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
          helper.populate()
        
    return process

def init_argparse():
    parser = make_parser("Handle random number seeding")
    parser.add_argument('--seeding', nargs='+', required=True)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    do_loop(args, handle_seeds)

main()
