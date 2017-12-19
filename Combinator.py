

class Combinator:
    sweeps = []

    def add_sweep(self, i, begin, end, step):
        self.sweeps = []
        self.sweeps.append((i, begin, end, step))
        # print(self.sweeps)

    def get_combinations(self):
        # ToDo: add functionality for multiple sweeps in parallel.
        combs = []
        if len(self.sweeps) == 1:
            sweep = self.sweeps[0]
            i, begin, end, step = sweep[0], sweep[1], sweep[2], sweep[3]
            print('%d %d %d %d' % (i, begin, end, step))
            while begin <= end:
                combs.append((i, begin))
                begin += step
                print("Begin: %d, End: %d, Bigger? %s" % (begin, end, begin <= end))

        return combs
