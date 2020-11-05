#!/bin/sh
echo "Running tests"
test_dir=`dirname "$0"`
cd $test_dir
test_dir=`pwd`
echo "Test dir is $test_dir"

# the psets are from CMSSW_10_6_4_patch1
cd `scram list CMSSW_10_6_4_patch1 | grep cvmfs | awk '{print $2}'`
eval `scramv1 runtime -sh`
cd $test_dir


rm -f pset_new.pkl
echo "Testing... param tweak"
$test_dir/../bin/edm_pset_tweak.py --json $test_dir/tweaks_test1.json --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl

if [ $? -eq 0 ]
then
  echo "Tweak applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param maxEvents.input --output out_param.json
else
  echo "Failed to apply tweak" >&2
fi


rm -f pset_new.pkl
echo "Testing... param tweak without override"
$test_dir/../bin/edm_pset_tweak.py --json $test_dir/tweaks_test1.json --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl --skip_if_set

if [ $? -eq 0 ]
then
  echo "Tweak applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param maxEvents.input --output out_param_skip.json
else
  echo "Failed to apply tweak" >&2
fi


echo ""
rm -f pset_new.pkl

# do GUID test
echo "Testing... guid"
$test_dir/../bin/cmssw_enforce_guid_in_filename.py --input_pkl $test_dir/digi.pkl --output_pkl pset_new.pkl --input_source source

if [ $? -eq 0 ]
then
  echo "GUID protection applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/digi.pkl pset_new.pkl --param source.enforceGUIDInFileName --output out_guid.json
else
  echo "Failed to add protection for GUID" >&2
fi

echo ""
rm -f pset_new.pkl

# do random test
echo "Testing... random"
$test_dir/../bin/cmssw_handle_random_seeds.py --input_pkl $test_dir/digi.pkl --output_pkl pset_new.pkl --seeding dud

if [ $? -eq 0 ]
then
  echo "Random seedings applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/digi.pkl pset_new.pkl --param RandomNumberGeneratorService.generator --output out_random.json
else
  echo "Failed test for random seeds" >&2
fi

echo ""
rm -f pset_new.pkl

# do random test reproductible
echo "Testing... random"
$test_dir/../bin/cmssw_handle_random_seeds.py --input_pkl $test_dir/digi.pkl --output_pkl pset_new.pkl --seeding ReproducibleSeeding --reproducible_json repro_random.json

if [ $? -eq 0 ]
then
  echo "Random seedings applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/digi.pkl pset_new.pkl --param RandomNumberGeneratorService.generator --output out_random_repro.json
else
  echo "Failed to set random seeds in reproducible test" >&2
fi

echo ""
rm -f pset_new.pkl

# do Condortest
echo "Testing... condor"
$test_dir/../bin/cmssw_handle_condor_status_service.py --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl --name step3

if [ $? -eq 0 ]
then
  echo "Condor applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param CondorStatusService.tag --output out_condor.json
else
  echo "Failed to add protection for GUID" >&2
fi
echo ""
rm -f pset_new.pkl

# do lazy download
echo "Testing... lazy download"
$test_dir/../bin/cmssw_enable_lazy_download.py --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl 

if [ $? -eq 0 ]
then
  echo "Lazy download applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param SiteLocalConfigService.overrideSourceCacheHintDir --output out_lazy.json
else
  echo "Lazy download to add protection for GUID" >&2
fi

echo ""
rm -f pset_new.pkl

# do dqmsaver
echo "Testing...dqmsaver"
$test_dir/../bin/cmssw_handle_dqm_filesaver.py --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl --multiRun --datasetName myDataset

if [ $? -eq 0 ]
then
  echo "Condor applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param dqmSaver.workflow dqmSaver.runIsComplete dqmSaver.forceRunNumber  --output out_dqm.json
else
  echo "Failed to add protection for dqmsaver" >&2
fi

echo ""
rm -f pset_new.pkl

# do create process
echo "Testing... Create process"
$test_dir/../bin/cmssw_wm_create_process.py --output_pkl pset_new.pkl --funcname merge --funcargs create_process.json

if [ $? -eq 0 ]
then
  echo "Create process applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl pset_new.pkl --param "_Process__name"  --output out_create_process.json
else
  echo "Failed to run create process" >&2
fi

echo ""
rm -f pset_new.pkl

# do pileup
echo "Testing... pileup"
$test_dir/../bin/cmssw_handle_pileup.py --input_pkl $test_dir/digi.pkl --output_pkl pset_new.pkl --pileup_dict pileup.json --skip_pileup_events 100

if [ $? -eq 0 ]
then
  echo "Pileup process applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl  pset_new.pkl --param "mixData.input.fileNames" --output out_pileup.json
else
  echo "Failed to run pileup process" >&2
fi

echo ""
rm -f pset_new.pkl
