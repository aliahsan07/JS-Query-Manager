/**
 *
 * @testcase_name prototype-3
 * @version 1.0
 * @description
 * @groundtruth_file prototype-3.ground
 */

function Person(n) {
  this.setName(n);
  Person.prototype.count++;
  this.m = [5];
}
Person.prototype.count = 0;
Person.prototype.setName = function (n) {
  this.name = n;
};

function Student(n, s) {
  this.b = Person;
  this.b(n);
  delete this.b;
  this.studentid = s.toString();
}
Student.prototype = new Person();

var x = new Student("Joe Average", 1);
delete x.m;
var y = new Person("Ali");
var z = x.m;
