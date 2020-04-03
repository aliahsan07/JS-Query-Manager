var foo = {};
var obj = { a: 1, b: 2 };

for (var name in obj) {
  var name_obj = { name: name };

  foo[name_obj.name] = obj[name_obj.name]; // Split on name_obj.name
}
