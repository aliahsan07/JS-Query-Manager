function f() {
  return {
    evalWorks: true
  };
}

var test = eval("f()");

var groundTruth = {
  "test-7": 1
};
