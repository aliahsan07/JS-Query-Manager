// test case 5
// for in loop, dynamic property read

var src = {
  alpha: 1,
  beta: "testing",
  gamma: new Boolean(true)
};

var dest = {};
for (var prop in src) {
  dest[prop] = src[prop];
}
