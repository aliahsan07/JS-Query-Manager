var src = {
  alpha: 1,
  beta: "testing",
  gamma: new Boolean(true)
};

var dest = {};
for (var prop in src) {
  dest[prop] = src[prop];
}

var groundTruth = {
  "prop-9": 3
};
