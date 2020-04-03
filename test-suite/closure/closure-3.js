function init() {
  var name = "Mozilla"; // name is a local variable created by init
  name = "Firefox";
  function displayName() {
    // displayName() is the inner function, a closure
    var toReturn = name;
    return toReturn; // use variable declared in the parent function
  }
  displayName();
}
init();
