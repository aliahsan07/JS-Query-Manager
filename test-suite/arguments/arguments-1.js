/**
 *
 * @testcase_name arguments-1
 * @version 1.0
 * @description
 * @groundtruth_file arguments-1.ground
 */
function testArguments(a) {
  var c = arguments[0];
  return c[1];
}

var ret = testArguments([1, 2, 3]);
