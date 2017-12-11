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
        if success:
            self.interactive = self.retrieve_interactive()
        else:
            self.interactive = None
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

    def add_sweep(self, i, begin, end, step):
        self.combinator.add_sweep(i, begin, end, step)

    def execute(self):
        combinations = self.combinator.get_combinations()
        print(combinations)
        for comb in combinations:
            i, val = comb[0], comb[1]
            param = self.interactive[i]
            print(self.interesting[param])
            if self.interesting[param] == 'declaration':
                changer = param[:].split('=')
                changer[-1] = "= " + val
                changer = ''.join(changer)
                print("%s, %s" % (param, changer))
