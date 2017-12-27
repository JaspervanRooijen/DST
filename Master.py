from IO import *
from Combinator import *
from Verifier import *
import os


class Master:
    io = IO()
    combinator = Combinator()
    verifier = Verifier()

    bs = None
    interesting = None
    interactive = None
    query = os.getcwd().replace("\\", "/")+"/tmp/TWES.q"    # Todo: make this adjustable

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
        result = {}
        combinations = self.combinator.get_combinations()
        # print(combinations)
        file = None
        for comb in combinations:
            # print('interactive = ' + str(self.interactive))
            i, val = comb[0], comb[1]
            param = self.interactive[i]
            # print('interesting[param] = ' + self.interesting[param])
            print('val = ' + str(val))
            # print('index = ' + str(i))
            # print('param = ' + param)
            if self.interesting[param] == 'declaration':
                changer = param[:].split('=')
                changer[-1] = "= " + str(val)
                changer = ''.join(changer)
                # print('changer = ' + changer)
                file = self.io.create_combination(param, changer)
            with open(self.query, 'r') as f:
                print(f.read())
            mean = self.verifier.verify(file, self.query)
            result[str(val)] = mean
        return result

    def get_sweeps(self):
        return self.combinator.get_sweeps()

    def simulate(self, amount, query):
        print('simulating!!')
        result = {}
        combinations = self.combinator.get_combinations()
        # print(combinations)
        file = None
        for comb in combinations:
            # print('interactive = ' + str(self.interactive))
            i, val = comb[0], comb[1]
            param = self.interactive[i]
            # print('interesting[param] = ' + self.interesting[param])
            print('val = ' + str(val))
            # print('index = ' + str(i))
            # print('param = ' + param)
            if self.interesting[param] == 'declaration':
                changer = param[:].split('=')
                changer[-1] = "= " + str(val)
                changer = ''.join(changer)
                # print('changer = ' + changer)
                file = self.io.create_combination(param, changer)
            # with open(self.query, 'r') as f:
            #     print(f.read())

            q = 'simulate %s [<=888] {%s}' % (str(amount), query)   #Todo: Fix hardcode final time

            res = self.verifier.simulate(file, q)
        return result


