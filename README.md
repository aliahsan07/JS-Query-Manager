Query Manager (for a lack of better word) is a Python engine that runs a JavaScript file against Static Analysis tools for pointer analysis. Specifically, it ouputs a points to set for source variables provided in the JS file. 
Currently, two tools are supported, TAJS and Safe. 

# How to run
```
python3 manager.py --test test-suite/object-sensitivity/object-sensitivity-3.js --safe --tajs
``` 

## Flags
- test: provide file to test against 
- safe: enable output by Safe
- tajs: enable output by TAJS

The output is then generated in output.yaml file

