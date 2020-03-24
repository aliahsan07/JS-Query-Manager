var src = {};
var dest = {};

var temp = null;
src[temp] = {}; // fix it for safe (prop values for ob)
src["ins"] = {};

var prop = Math.random() > 0.5 ? "ext" : "ins";

var t = src[prop];

dest[prop] = t;
