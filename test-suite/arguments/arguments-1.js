function testArguments(a, b) {
  var c = arguments[1];
  return c;
}

var ret = testArguments(1, 2);
