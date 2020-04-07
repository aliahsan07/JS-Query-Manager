function testArguments(a) {
  var c = arguments[0];
  return c[1];
}

var ret = testArguments([1, 2, 3]);

var groundTruth = {
  "arguments-1": 1
};
