/**
 *
 * @testcase_name alias-1
 * @version 1.0
 * @description
 * @groundtruth_file alias-1.ground
 */

function evalAlias(dest) {
  var result = dest.roll * 5;
  return result;
}

var src = { text: "UTD", roll: 23 };
var test = evalAlias(src);
