function extend(destination, source) {
  for (var property in source) destination[property] = source[property];
  return destination;
}

extend(Object, {
  extend: extend,
  inspect: inspect,
});

Object.extend(
  String.prototype,
  (function () {
    function capitalize() {
      return this.charAt(0).toUpperCase() + this.substring(1).toLowerCase();
    }
    function empty() {
      return this == "";
    }
    return {
      capitalize: capitalize,
      empty: empty,
    };
  })()
);
" javaScript ".capitalize(); // == "Javascript"
