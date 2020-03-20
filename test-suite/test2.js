function Student(name) {
  this.name = name;
  Student.prototype.count++;
}

Student.prototype.count = 0;

var x = new Student("Ali Ahsan");
var y = new Student("John Doe");
