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

var t2 = t;

var groundTruth = {
  "t2-10": 2,
  "ext-12": 1,
  "ins-13": 1,
};
