# cmssw-wm-tools
Repository for release independent tools to glue together cmssw, wmagent, and wmcontrol for workflow submission use cases

Currently there are two tools

1.
```edm_pset_tweak.py --input_pkl RunPromptRecoCfg.pkl --output_pkl ouput.pkl --json tweaks.json```

tweaks.json can be
```  [{ "process.maxEvents.input" : 100}]```
or
``` { "process.maxEvents.input" : 100}```
or
``` [{ "maxEvents.input" : 100}]```
or
``` { "maxEvents.input" : 100}```
 
 properly handles multiple pkls and mulitple jsons (all jsons are applied to all pkls)

2. tweak_maker_lite which contains the TweakMakerLite class
