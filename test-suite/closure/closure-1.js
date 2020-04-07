function makeGetter(x) {
  function inner(y) {
    return x[y];
  }
  return inner;
}

var temp = makeGetter([1, 2, 3]);
var val = temp(1);

var groundTruth = {
  "temp-8": 1,
  "inner-5": 1
};
