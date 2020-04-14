var t = {
  [24]: [1, 2, 3],
  [1]: { c: 3 }
};

var c = {};

for (var prop in t) {
  c[prop] = t[prop];
}

var t1 = c[prop];
var t2 = prop;

var groundTruth = {
  "t1-12": 1,
  "t2-13": 1
};
