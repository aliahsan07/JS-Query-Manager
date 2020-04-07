var x = {};
var z = x.f;
x.f = {};

var groundTruth = {
  "f-3": 1,
  "x-1": 1,
  "z-3": 0
};
