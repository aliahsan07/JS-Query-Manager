function evalAlias(dest) {
  var result = dest.roll * 5;
  return result;
}

var src = { text: "UTD", roll: 23 };
var test = evalAlias(src);

// INSTRUMENTATION LIKE. ASK PROF
var groundTruth = {
  "dest-2": 1,
  "src-6": 1
};

// instead
// var groundTruth = {
// "dest-2": ["src-6"]
//}
