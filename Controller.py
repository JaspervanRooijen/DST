from View import *
from Master import *


class Controller:
    view = TuiView()
    master = Master()

    def main(self):
        while True:
            command = input('>').split(" ")
            if command[0] == 'openFile':
                if self.master.open_file(command[1]):
                    print('File %s opened' % command[1])
                else:
                    print('Filename unknown, failed opening...')
            elif command[0] == 'parameters':
                parameters = self.master.get_parameters()
                interactive = self.master.get_interactive()
                bs = self.master.get_bs()
                self.view.show_parameters(parameters, interactive, bs)
            elif command[0] == 'sweep':
                Combinator.add_sweep(command[1], command[2], command[3], command[4])
                # sweeps.append([command[1], command[2], command[3], command[4]])
                return
            elif command[0] == 'execute':
                # execute2(bs, interesting, interactive, sweeps, controller)
                return
            elif command[0] == 'print':
                # print(bs)
                # elif command[0] == 'reload':
                #	imp.reload(datasweep)
                return
            elif command[0] == 'show':
                # return
                return
            elif command[0] == 'exit':
                self.master.close_file()
                # if f is not None:
                #     f.close()
                #     print("Closed file %s" % filename)
                return
