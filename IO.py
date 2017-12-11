from File import *

class IO:
    file = File()
    bs = None
    interesting = None

    def open_file(self, file):
        if self.file.open_file(file):
            self.bs = self.file.get_bs()
            self.interesting = self.get_parameters()
            return True, self.bs, self.interesting
        else:
            return False, None, None

    def get_parameters(self):
        if self.interesting is not None:
            return self.interesting
        else:
            interesting = dict()
            # Find all transitions
            transitions = self.bs.findAll('transition')
            for trans in transitions:
                for label in trans.findAll('label'):
                    if label['kind'] == 'probability':
                        interesting[trans] = 'transition'
                        # print("Added: %s \n" % trans)

            # Find all ints in the global declarations
            for decl in str(self.bs.findAll('declaration')).split('\n'):
                if decl[:4] == 'int ':
                    interesting[decl.split(';')[0]] = 'declaration'
                if decl[:10] == 'const int ':
                    # print("Added: %s \n" % decl.split(';')[0])
                    interesting[decl.split(';')[0]] = 'declaration'

            self.interesting = interesting
            return interesting

    def close_file(self):
        self.bs = None
        self.interesting = None
        self.file.close_file()
        print('Program closed correctly')
