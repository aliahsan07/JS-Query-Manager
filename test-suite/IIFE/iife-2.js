/**
 *
 * @testcase_name iife-1
 * @version 1.0
 * @description
 * @groundtruth_file iife-1.ground
 */

var x = {};

(function () {
  var x = [];
})();

var t1 = x;
