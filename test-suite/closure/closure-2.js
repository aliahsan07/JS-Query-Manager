function init() {
  var name = Math.random() > 0.5 ? "ext" : "ins";
  function displayName() {
    alert(name);
  }
  displayName();
}
init();
