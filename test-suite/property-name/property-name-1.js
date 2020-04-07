var foo = {};
var obj = { a: {}, b: {} };

for (var name in obj) {
  var name_obj = { name: name };

  foo[name_obj.name] = obj[name_obj.name];
}

var groundTruth = {
  "foo-7": 1
};
