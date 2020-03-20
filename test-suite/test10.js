// test 10
// inheritance
function Wheel4() {
  this.wheel = 4;
}
function Car() {
  this.maxspeed = 200;
}

Car.prototype = new Wheel4();
var modernCar = new Car();

console.log(modernCar instanceof Car);

function Wheel6() {
  this.wheel = 6;
}

Car.prototype = new Wheel6();

var afterModern = modernCar instanceof Car; // false

var truck = new Car();

var aftertruck = truck instanceof Car; // true
