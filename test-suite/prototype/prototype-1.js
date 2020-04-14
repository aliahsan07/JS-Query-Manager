var Person = {
  m: [5]
};
var y = Object.create(Person);
var z = y.m;

delete Person.m;
var z = y.m;

var groundTruth = {
  "z-8": 0
};
