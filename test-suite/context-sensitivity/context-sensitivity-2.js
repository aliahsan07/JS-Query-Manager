function testCxtSen(property, obj) {
  return obj[property];
}

var obj = {
  first: [1, 2, 3],
  second: new String("any string"),
  third: {}
};

for (var prop in obj) {
  obj[prop] = testCxtSen(prop, obj);
}

var secondObj = obj["second"];

var groundTruth = {
  "secondObj-15": 1
};
