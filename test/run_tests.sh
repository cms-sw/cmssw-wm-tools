#!/bin/sh
echo "Running tests"
test_dir=`dirname "$0"`
echo $test_dir
edm_pset_tweak.py --json $test_dir/tweaks_test1.json --input_pkl $test_dir/pset1.pkl --output_pkl pset_new.pkl

if [ $? -eq 0 ]
then
  echo "Tweak applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/pset1.pkl pset_new.pkl --param maxEvents.input
else
  echo "Failed to apply tweak" >&2
fi

rm -f pset_new.pkl
