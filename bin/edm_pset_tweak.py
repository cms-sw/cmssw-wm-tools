#!/usr/bin/env python
# usage
# edm_pset_tweak.py --input_pkl RunPromptRecoCfg.pkl --output_pkl ouput.pkl --json tweaks.json
#
# tweaks.json can be
#  [{ "process.maxEvents.input" : 100}]
# or
# { "process.maxEvents.input" : 100}
# or
# [{ "maxEvents.input" : 100}]
# or
# { "maxEvents.input" : 100}
# 
# properly handles multiple pkls and mulitple jsons (all jsons are applied to all pkls)
#

import FWCore.ParameterSet.Config as cms
import pickle
try: 
   import argparse
except ImportError: #get it from this package instead
   import archived_argparse as argparse 
import sys
import json

def convert_unicode_to_str(data):
    PY3 = sys.version_info[0] == 3
    if PY3:
        return data
    if type(data) in (int, float, str, bool):
            return data
    elif type(data) == unicode:
            return str(data)
    elif type(data) in (list, tuple, set):
            data = list(data)
            for i,v in enumerate(data):
                    data[i] = convert_unicode_to_str(v)
    elif type(data) == dict:
            for i,v in data.iteritems():
                    data[i] = convert_unicode_to_str(v)
    else:
            print("invalid dataect in data, converting to string")
            data = str(data) 
    return data

def apply_tweak(process, key, value, skip_if_set):
    value = convert_unicode_to_str(value)
    # Allow setting specific types from json
    if isinstance(value, str):
        value_split = value.split('.')
        if value_split[0] == "customTypeCms":
            value = eval('cms.{0}'.format('.'.join(value_split[1:])))
    key_split = key.split('.')
    param=process
    if key_split[0] == "process":
        key_split = key_split[1:]
    for p in key_split[:-1]:
        if not hasattr(param,p):
            return 1
        param = getattr(param, p)
        if param is None:
            return 1
    if skip_if_set and hasattr(param,key_split[-1]): 
       print("Attribute already set "+key+". Not changing")
       return 0
    setattr(param,key_split[-1],value)
    print("Set attribute "+key+" to "+str(getattr(param,key_split[-1])))
    return 0


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Tweak pset(s) based on json list of tweaks to apply and write out resulting pset(s)"
    )
    parser.add_argument('--json', nargs='+', required=True)
    parser.add_argument('--input_pkl', nargs='+', required=True)
    parser.add_argument('--output_pkl', nargs='+', required=False)
    parser.add_argument('--allow_failed_tweaks', action='store_true')
    parser.add_argument('--skip_if_set', action='store_true')
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()
    if len(args.output_pkl) != 0:
        output_file_names = args.output_pkl
        if len(args.input_pkl) != len(args.output_pkl):
            print(
                "Incorrect arguments. --input_pkl and --output_pkl must be the same length")
            sys.exit(1)
    else:
        output_file_names=args.input_pkl

    tweaks = []
    for json_file_name in args.json:
        try:
            with open(json_file_name) as json_file:
                json_data = json.load(json_file)
        except Exception as e:
            print("Error opening file "+json_file_name)
            sys.exit(1)

        if not isinstance(json_data,(dict,list)):
            print("Error loading json "+json_file_name)
            sys.exit(1)

        if isinstance(json_data, list):
            for d in json_data:
                for key in d:
                    tweaks.append((key, d[key]))
        elif isinstance(json_data, dict):
            for key in json_data:
                tweaks.append((key, json_data[key]))
        else:
            print("Error loading json "+json_file_name)
            sys.exit(1)

    for i in range(len(args.input_pkl)):
        with open(args.input_pkl[i], "rb") as pkl_file:
            try:
                process = pickle.load(pkl_file)
            except (IOError, OSError, pickle.PickleError, pickle.UnpicklingError):
                print("Not a valid pickle file " +
                      args.input_pkl[i]) + "- stopping"
                sys.exit(1)

        for tweak in tweaks:
            err_val = apply_tweak(process, tweak[0], tweak[1],args.skip_if_set)
            if err_val != 0:
                print("Tweak not applied "+tweak[0]+" "+str(tweak[1]))
                if not args.allow_failed_tweaks:
                    sys.exit(1)

        with open(output_file_names[i], "wb") as output_file:
            if output_file.closed:
                print("Error loading pickle input "+args.output_pkl[i])
                sys.exit(1)
            pickle.dump(process, output_file, protocol=0)


main()

