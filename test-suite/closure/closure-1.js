/**
 *
 * @testcase_name closure-1
 * @version 1.0
 * @description
 * @groundtruth_file closure-1.ground
 */

function makeGetter(x) {
  function inner(y) {
    return x[y];
  }
  return inner;
}

var temp = makeGetter([1, 2, 3]);
var val = temp(1);
