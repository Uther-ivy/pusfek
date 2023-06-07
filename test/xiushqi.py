class Person:
    age = 25

    @classmethod
    def printAge(self):
        print('The age is:', self.age)
Person.printAge = classmethod(Person.printAge)

Person.printAge()


