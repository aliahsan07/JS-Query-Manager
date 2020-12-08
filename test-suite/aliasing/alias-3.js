/**
 *
 * @testcase_name alias-2
 * @version 1.0
 * @description
 * @groundtruth_file alias-2.ground
 */

var src = {};
var dest = {};

src["ext"] = {};
src["ins"] = {};

var prop = Math.random() > 0.5 ? "ext" : "ins";

var t = src[prop];
