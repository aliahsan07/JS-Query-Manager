# JavaScript Pointer Analysis Querier 
JS Pointer Analysis Querier is a Python engine that runs JavaScript file(s) against Static Analysis tools for pointer analysis. Specifically, it ouputs a points to set for source variables provided in the JS file. 
Currently, two tools are supported, [TAJS](https://github.com/cs-au-dk/TAJS) and [Safe](https://github.com/sukyoung/safe). 

## Ground Truth
We define the ground truth as how many heap locations does the variable point to at the runtime. 

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

## Note on WALA

Currently, I dont have a scripty way to invoke the points to set on WALA which means running this Python script wont actually query WALA (it works for other two tools). To get results for WALA, I run the [WALA start](https://github.com/wala/WALA-start) script provided by the WALA team. I extract the IR variables for the source variables and then use the points-to set abstraction provided by WALA to get the required points to information. 

### [](#list-of-tests)List of tests

| Type                | No. of Tests |
| ------------------- | :----------: |
| Aliasing            |      3       |
| Closures            |      3       |
| Eval                |      3       |
| With                |      3       |
| IIFE                |      2       |
| Arguments Array     |      1       |
| Dynamic Properties  |      5       |
| Prototype           |      6       |
| Flow Sensitivity    |      2       |
| Context Sensitivity |      3       |
| Object Sensitivity  |      3       |