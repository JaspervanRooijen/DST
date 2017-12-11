from IO import *
from Combinator import *


class Master:
    io = IO()
    combinator = Combinator()

    bs = None
    interesting = None
    interactive = None

    def open_file(self, file):
        success, self.bs, self.interesting = self.io.open_file(file)
        self.interactive = self.retrieve_interactive()
        return success

    def close_file(self):
        self.io.close_file()

    def get_parameters(self):
        return self.interesting

    def retrieve_interactive(self):
        interactive = []
        for interest in self.interesting:
            interactive.append(interest)
        return interactive

    def get_interactive(self):
        return self.interactive

    def get_bs(self):
        return self.bs

