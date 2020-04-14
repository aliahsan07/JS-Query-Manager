var x;

var y = {
  a: [1, 2],
  b: [3, 4, 5]
};

for (var c in y) {
  x = y[c];
}

var test = x;

var groundTruth = {
  "test-12": 1
};
