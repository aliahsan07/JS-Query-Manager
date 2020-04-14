var x = {
  c: {}
};

var t1 = x.c;

(function () {
  x.c = [];
})();

t1 = x.c;

var groundTruth = {
  "t1-5": 1,
  "t1-11": 1
};
