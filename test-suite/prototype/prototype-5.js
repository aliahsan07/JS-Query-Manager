var a = {
  a: {}
};

var b = Object.create(a);
b.a = [];

var c = b.a;

delete b.a;
c = b.a;
delete a.a;
c = b.a;

var groundTruth = {
  "c-8": 1,
  "c-11": 1,
  "c-13": 0
};
