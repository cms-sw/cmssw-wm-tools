#!/usr/bin/env python
import sys, os
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '..', 'python'))

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError:  #get it from this package instead
   import archived_argparse as argparse 
import re, os
import json

from tweak_program_helpers import make_parser

#https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json/33571117#33571117
def byteify(data, ignore_dicts = False):
    if isinstance(data, str):
        return data

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ byteify(item, ignore_dicts) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    # DL: Changed - we dont want unicode anywhere...
    if isinstance(data, dict) and not ignore_dicts:
        return {
#            byteify(key, ignore_dicts=True): byteify(value, ignore_dicts=True)
            byteify(key, ignore_dicts): byteify(value, ignore_dicts)
            for key, value in data.items() 
        }

    # python 3 compatible duck-typing
    # if this is a unicode string, return its string representation
    if str(type(data)) == "<type 'unicode'>":
        return data.encode('utf-8')

    # if it's anything else, return it in its original form
    return data

def create_process(args,func_args):
   
   if args.funcname == "merge":
      if args.useErrorDataset:
         func_args['outputmod_label'] = "MergedError"
         
      try:
         from Configuration.DataProcessing.Merge import mergeProcess
         process = mergeProcess(**func_args)
      except Exception as ex:
         msg = "Failed to create a merge process."
         print(msg)
         raise ex
   elif args.funcname == "repack":
      try:
         from Configuration.DataProcessing.Repack import repackProcess
         process = repackProcess(**func_args)
      except Exception as ex:
         msg = "Failed to create a repack process."
         print(msg)
         raise ex
   else:
      try:
         from Configuration.DataProcessing.GetScenario import getScenario
         scenario = func_args['scenario']
         scenarioInst = getScenario(scenario)
      except Exception as ex:
         msg = "Failed to retrieve the Scenario named "
         msg += str(scenario)
         msg += "\nWith Error:"
         msg += str(ex)
         print(msg)
         raise ex
      try:
         my_func=getattr(scenarioInst, args.funcname)
         arg_names=my_func.func_code.co_varnames[1:1+my_func.func_code.co_argcount]
         #the last arg should be **args - get the others from the dictionary passed in
         arg_names=arg_names[:-1]
         call_func_args=[]
         for name in arg_names:
            call_func_args.append(func_args[name])
            del func_args[name]
         process = my_func(*call_func_args, **func_args)
      except Exception as ex:
         msg = "Failed to load process from Scenario %s (%s)." % (scenario, scenarioInst)
         print(msg)
         raise ex
      
   return process

def init_argparse():
   parser = argparse.ArgumentParser(
      usage="%(prog)s [OPTION] [FILE]...",
      description="Process creator (merge, DataProcessing etc)"
   )
   
   parser.add_argument('--funcname', required=True)
   parser.add_argument('--funcargs', required=True)
   parser.add_argument('--useErrorDataset', action="store_true", required=False)
   parser.add_argument('--output_pkl', required=True)
   return parser


def main():
   parser = init_argparse()
   args = parser.parse_args()
   
   func_args={}
   
   try:
      with open(args.funcargs) as json_file:
         string = json_file.read()
         json_data = json.loads(string)
         json_data = byteify(json_data)
   except Exception as e:
      print("Error opening file "+args.funcargs)
      sys.exit(1)
         
   if not isinstance(json_data,dict):
      print("Error loading dictionary "+args.funcargs)
      sys.exit(1)

   func_args = json_data

   process=create_process(args, func_args)

   with open(args.output_pkl, "wb") as output_file:
      if output_file.closed:
         print("Error loading pickle input "+args.output_pkl[i])
         sys.exit(1)
      pickle.dump(process, output_file, protocol=0)
         

main()
