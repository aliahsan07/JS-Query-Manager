var test = {
  a: {
    b: { c: 100 },
    d: { e: 200 }
  }
};

var t1 = test.a.b;
var t2 = test.a.d;
with (test.a) {
  b = { f: 101 };
}

t1 = test.a.b;
t2 = test.a.d;

var groundTruth = {
  "t1-8": 1,
  "t2-9": 1,
  "t1-14": 1,
  "t2-15": 1
};
