/**
 *
 * @testcase_name iife-1
 * @version 1.0
 * @description
 * @groundtruth_file iife-1.ground
 */

var x = {
  c: {},
};

var t1 = x.c;

(function () {
  x.c = [];
})();

t1 = x.c;
