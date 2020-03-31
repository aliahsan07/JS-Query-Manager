function evalAlias(dest) {
  var result = dest.roll * 5;
  return result;
}

var src = { text: "UTD", roll: 23 };
var test = evalAlias(src);
