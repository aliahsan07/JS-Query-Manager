var t = {
  a: [1, 2, 3],
  b: { c: 3 }
};

var c = {};

for (var prop in t) {
  c[prop] = t[prop];
}

var t1 = c.a;

var groundTruth = {
  "t1-12": 1
};
