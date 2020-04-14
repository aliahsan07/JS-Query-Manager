var Person = {
  m: [5]
};
var y = Object.create(Person);
var z = y.m;
y.m = [10];

var groundTruth = {
  "m-2": 1,
  "z-5": 1,
  "m-6": 1
};
