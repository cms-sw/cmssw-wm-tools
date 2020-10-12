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

# do GUID test
cmssw_enforce_guid_in_filename.py --input_pkl $test_dir/pset1.pkl --output_pkl pset_new.pkl --input_source source

if [ $? -eq 0 ]
then
  echo "GUID protection applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/pset1.pkl pset_new.pkl --param source.enforceGUIDInFileName
else
  echo "Failed to add protection for GUID" >&2
fi


# do GUID test
cmssw_handle_random_seeds.py --input_pkl $test_dir/pset1.pkl --output_pkl pset_new.pkl --seeding dud

if [ $? -eq 0 ]
then
  echo "Random seedings applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/pset1.pkl pset_new.pkl --param source.RandomNumberGeneratorService
else
  echo "Failed to add protection for GUID" >&2
fi
