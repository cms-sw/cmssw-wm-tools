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
echo "guid"
cmssw_enforce_guid_in_filename.py --input_pkl $test_dir/digi.pkl --output_pkl pset_new.pkl --input_source source

if [ $? -eq 0 ]
then
  echo "GUID protection applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/digi.pkl pset_new.pkl --param source.enforceGUIDInFileName
else
  echo "Failed to add protection for GUID" >&2
fi


# do random test
echo "Random"
cmssw_handle_random_seeds.py --input_pkl $test_dir/digi.pkl --output_pkl pset_new.pkl --seeding dud

if [ $? -eq 0 ]
then
  echo "Random seedings applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/digi.pkl pset_new.pkl --param source.RandomNumberGeneratorService
else
  echo "Failed to add protection for GUID" >&2
fi


# do Condortest
echo "condor"
cmssw_handle_condor_status_service.py --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl --name step3

if [ $? -eq 0 ]
then
  echo "Condor applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param CondorStatusService.tag
else
  echo "Failed to add protection for GUID" >&2
fi

# do lazy download
echo "lazy download"
cmssw_enable_lazy_download.py --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl 

if [ $? -eq 0 ]
then
  echo "Condor applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param SiteLocalConfigService.overrideSourceCacheHintDir
else
  echo "Failed to add protection for GUID" >&2
fi

# do dqmsaver
echo "dqmsaver"
cmssw_handle_dqm_filesaver.py --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl --multiRun --datasetName myDataset

if [ $? -eq 0 ]
then
  echo "Condor applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/reco.pkl pset_new.pkl --param dqmSaver.workflow dqmSaver.runIsComplete dqmSaver.forceRunNumber
else
  echo "Failed to add protection for GUID" >&2
fi


# do create process
echo "Create process"
cmssw_wm_create_process.py --output_pkl pset_new.pkl --funcname merge --funcargs create_process.json

if [ $? -eq 0 ]
then
  echo "Create process applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl pset_new.pkl --param "name"
else
  echo "Failed to run create process" >&2
fi

# do pileup
echo "Pileup"
cmssw_handle_pileup.py --input_pkl $test_dir/digi.pkl --output_pkl pset_new.pkl --pileup_dict pileup.json --skip_pileup_events 100

if [ $? -eq 0 ]
then
  echo "Pileup process applied ok, lets check it"
  $test_dir/get_pset_param.py --input_pkl $test_dir/digi.pkl pset_new.pkl --param "name"
else
  echo "Failed to run pileup process" >&2
fi

