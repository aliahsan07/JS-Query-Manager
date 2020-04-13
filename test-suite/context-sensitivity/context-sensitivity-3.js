function TestObject(t) {
  function closure() {
    return t;
  }

  return closure;
}

var x = TestObject([]);
var y = TestObject({});

var X = x();
var Y = y();

var groundTruth = {
  "X-12": 1,
  "Y-13": 1
};
