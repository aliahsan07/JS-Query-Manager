var src = {};
var dest = {};

src["ext"] = {};
src["ins"] = {};

var prop = Math.random() > 0.5 ? "ext" : "ins";

var t = src[prop];

var t2 = t;

var groundTruth = {
  "t2-11": 2
};
