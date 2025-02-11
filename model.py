class Person:

    def __init__(self):
        self.name = "Andrew"

    def change_name(self):
        self.name = self.name + "a"

    def get_name(self):
        return self.name