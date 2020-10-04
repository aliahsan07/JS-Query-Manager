# JS Query Manager
Query Manager (for a lack of better word) is a Python engine that runs a JavaScript file against Static Analysis tools for pointer analysis. Specifically, it ouputs a points to set for source variables provided in the JS file. 
Currently, two tools are supported, [TAJS](https://github.com/cs-au-dk/TAJS) and [Safe](https://github.com/sukyoung/safe). 

## Requirements
- Python 3.8 or later

## How to run

Before you run the python script, you need to setup environment variable for Safe to run. The safe binaries are located inside the /Safe/bin directory of this repository. In your shell startup script, add LocationOfThisRepo/Safe/bin to your path.

To test whether safe is working, run:
`safe help` 
This will show a list of commands supported by the Safe framework if its in the path.

First, install dependencies with pip3:
`pip3 install -r requirements.txt`

Before we run the python script that invokes JavaScript analysis tools, take a look at the flags currently supported:
- --test (string): JavaScript source file to run analysis on
- --safe (boolean): Provide the flag to enable analysis by Safe
- --tajs (boolean): Provide the flag to enable analysis by TAJS
- --safeConfig(string): Provide a config file to run custom configuarion of Safe
- --tajsConfig(string): Provide a config file to run custom configuration of TAJS
- --watch(boolean): Run all test cases one by one 

For example to run with default config:
```
python3 manager.py --test test-suite/prototype/prototype-5.js --safe --tajs
``` 


To run with custom config:
```
python3 manager.py --test test-suite/prototype/prototype-5.js --safe --tajs --safeConfig safeConfig.json --tajsConfig tajsConfig.json 
``` 

To run all test cases:
```
python3 manager.py --watch --safe --tajs
```

## Output Structure
The script after running outputs a yaml file in the out directory with the format out/{inputFileName}.yaml.
The output file generated after running the script on prototype-5 file is as follows:

### Output File Sample
```
files:
- filename: test-suite/prototype/prototype-5.js
  pointers:
  - groundTruth: 1
    lineNumber: 8
    safe:
      output:
      - '#8:Sens[(20-CFA()|LSA[i:10,j:100]())]'
      pointsToSize: 1
      precision: 1.0
      runtime: ' 0.0012'
    tajs:
      output:
      - '@Array#node24'
      pointsToSize: 1
      precision: 1.0
      runtime: ' 0.0014'
    varname: c
```

## Roadmap

There are a couple of things I'm working on right now. First and foremost is integrating the [WALA](https://github.com/wala/WALA) into the toolchain. It will be supported in the same way with flags deciding whether to run it on a file or not. Also, working on dockerizing the images instead of providing binaries and jar files for tools. 

