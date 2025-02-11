class Controller:

    def __init__(self, person):
        self.person = person
        pass

    def print_hello_world(self):
        self.person.change_name()
        print(self.person.get_name())