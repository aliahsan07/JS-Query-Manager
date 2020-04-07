function baseContextSensitivity(x) {
  return x;
}
var a = baseContextSensitivity({ A: "A" });
var d = baseContextSensitivity({ B: "B" });

var groundTruth = {
  "a-4": 1,
  "d-5": 1
};
