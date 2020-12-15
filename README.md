# cmssw-wm-tools
Repository for release independent tools to glue together cmssw, wmagent, and wmcontrol for workflow submission use cases

Currently there are nine tools

1. Apply tweaks to PSets
```
edm_pset_tweak.py --input_pkl RunPromptRecoCfg.pkl --output_pkl ouput.pkl --json tweaks.json
```

tweaks.json can be
```  [{ "process.maxEvents.input" : 100}]```
or
``` { "process.maxEvents.input" : 100}```
or
``` [{ "maxEvents.input" : 100}]```
or
``` { "maxEvents.input" : 100}```
 
 properly handles multiple pkls and mulitple jsons (all jsons are applied to all pkls). It has an option (skip_if_set) to skip tweaks if the parameter is already present (eg, [for case link this one](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py#L59-L68)).  
 
For this script and the ones, below, the output pkl options can be either empty (overwrite the input) or one output file per input file.
 
2. Enable lazy download when possible, as in [WMCore handleSpecialCERNMergeSettings](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py#L613-L629).
```
cmssw_enable_lazy_download.py --input_pkl reco.pkl --output_pkl pset_new.pkl 
```

3. Adjust GUID when possible, as in [WMCore handleEnforceGUIDInFileName](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py#L644-L684).
```
cmssw_enforce_guid_in_filename.py --input_pkl digi.pkl --output_pkl pset_new.pkl --input_source source
```

4. Enable condor service when possible, as in [WMCore handleCondorStatusService](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py#L631-L642)
```
cmssw_handle_condor_status_service.py --input_pkl $test_dir/reco.pkl --output_pkl pset_new.pkl --name step3
```

5. Handle dqm setup manipulation as in [WMCore handleDQMFileSaver](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py#L532-L562).
```
cmssw_handle_dqm_filesaver.py --input_pkl reco.pkl --output_pkl pset_new.pkl --multiRun --datasetName myDataset
```

Arguments include ```--multiRun``` (true if argument given), ```--datasetName``` (string), ```--runIsComplete``` (true if argument given), and ```--runLimits``` (string).

6. Support [the handlePileup use case in WMCore](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py#L376-L493).
```
cmssw_handle_pileup.py  --input_pkl digi.pkl --output_pkl pset_new.pkl --pileup_dict pileup.json --skip_pileup_events 100
```

The json file contains 
```
{ "data" : { "eventsAvailable" : 10000,
	     "FileList" : ["dud.root", "foo.root"]
	   },
  "mc" :   { "eventsAvailable" : 50000,
	     "FileList" : ["dud_mc.root", "mc_foo.root"]
	   }
}
```

7. Populate random number seeds
```
cmssw_handle_random_seeds.py --input_pkl digi.pkl --output_pkl pset_new.pkl --seeding ReproducibleSeeding --reproducible_json repro_random.json
```

The ```--reproducible_json``` option is needed only if ```--seeding``` is ```ReproducibleSeeding```. Multiple ```--seeding``` parameters are supported.

8. Replace the Tier-0 interfaces in [WMCore createProcesses](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py#L192-L237).
```
cmssw_wm_create_process.py --output_pkl pset_new.pkl --funcname merge --funcargs create_process.json
```

The ```funcname``` argument identifies which function to be called and the ```funcargs``` argument points to a json file with all of the arguments to be passed into that function. Eg,
```
{
 "scenario" : "ppRun2"
}
```

9. tweak_maker_lite which contains the TweakMakerLite class

10. Tweak any producers with the parameter nEvents to match the max_events of the process.
```
cmssw_handle_nEvents.py --input_pkl digi.pkl --output_pkl pset_new.pkl 
```
