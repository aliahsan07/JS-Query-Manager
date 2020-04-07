function foo(obj) {
  var prefix = "Hello ";
  with (obj) {
    console.log(prefix + msg);
  }
}

o1 = { msg: "World" };
foo(o1); // ’Hello World’

var groundTruth = {
  "obj-3": 1,
  "o1-8": 1
};
