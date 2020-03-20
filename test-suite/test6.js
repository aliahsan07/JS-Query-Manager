// test case 6
// with statement

function foo(obj) {
  var prefix = "Hello ";
  with (obj) {
    console.log(prefix + msg);
  }
}
foo({ msg: "World " }); // ’Hello World’
foo({ prefix: "Greetings ", msg: "Universe " });
