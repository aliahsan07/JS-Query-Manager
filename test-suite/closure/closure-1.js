function makeGetter(x) {
  function inner(y) {
    return x[y];
  }
  return inner;
}

var temp = makeGetter([1, 2, 3]);
var val = temp(1);
