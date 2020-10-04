/**
 *
 * @testcase_name context-sensitivity-3
 * @version 1.0
 * @description
 * @groundtruth_file context-sensitivity-3.ground
 */

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
