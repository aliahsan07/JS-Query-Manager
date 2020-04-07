function foo(obj) {
  with (obj) {
    a = { a: 2 };
  }
}

var o1 = {
  a: { a: 3 }
};

var o2 = {
  b: { b: 3 }
};

foo(o1);

foo(o2);
o1.a;
o2.a; // undefined
a; // leaked global

var groundTruth = {
  "a-18": 1,
  "a-19": 0,
  "a-20": 1
};
