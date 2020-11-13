#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import sys, re, os

from tweak_program_helpers import make_parser, do_loop, get_cmssw_version, isCMSSWSupported

def read_json(f):
   import json
   try:
      with open(f) as json_file:
         json_data = json.load(json_file)
   except Exception as e:
      print("Error opening file "+f)
      sys.exit(1)
         
   if not isinstance(json_data,dict):
      print("Error loading dictionary "+f)
      sys.exit(1)

   return json_data

def handle_seeds(process, args):

    seedings = args.seeding

    if not hasattr(process, "RandomNumberGeneratorService"):
       return process

    for seeding in seedings:
       if seeding == "ReproducibleSeeding":
          init_seeds = read_json(args.reproducible_json)
          randService = process.RandomNumberGeneratorService
          for x in randService.parameters_():
             if hasattr(getattr(randService,x),"initialSeed"):
                getattr(process.RandomNumberGeneratorService,x).initialSeed = init_seeds[x]
          print("Recalled random seeds from saved seeds")
       else:
          from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
          helper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
          helper.populate()
          print("Populared random numbers of RandomNumberService")
    return process

def init_argparse():
    parser = make_parser("Handle random number seeding")
    parser.add_argument('--seeding', nargs='+', required=True)
    parser.add_argument('--reproducible_json', required=False)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    if "ReproducibleSeeding" in args.seeding and args.reproducible_json is None:
       print("--reproducible_json argument is required if seeding type is ReproducibleSeeding")
       sys.exit(1)

    do_loop(args, handle_seeds)

main()
