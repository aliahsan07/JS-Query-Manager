Query Manager (for a lack of better word) is a Python engine that runs a JavaScript file against Static Analysis tools for pointer analysis. Specifically, it ouputs a points to set for source variables provided in the JS file. 
Currently, two tools are supported, TAJS and Safe. 

# How to run
```
python3 manager.py --test test-suite/object-sensitivity/object-sensitivity-3.js --safe --tajs
``` 

## Flags
- test: provide file to test against 
- safe: enable analysis by Safe
- tajs: enable analysis by TAJS

The output is then generated in output.yaml file

## Output File Sample
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
    tajs:
      output:
      - '@Array#node24'
      pointsToSize: 1
      precision: 1.0
    varname: c
  - groundTruth: 0
    lineNumber: 13
    safe:
      output: []
      pointsToSize: 0
      precision: 1.0
    tajs:
      output: []
      pointsToSize: 0
      precision: 1.0
    varname: c
```
