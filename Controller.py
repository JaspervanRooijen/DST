from View import *
from Master import *


class Controller:
    view = TuiView()
    master = Master()

    def main(self):
        # try:
            while True:
                command = input('>').split(" ")
                if command[0] == 'openFile':
                    # print(command[1])
                    if self.master.open_file(command[1]):
                        print('File %s opened' % command[1])
                    else:
                        print('Filename unknown, failed opening...')
                    continue
                elif command[0] == 'parameters':
                    parameters = self.master.get_parameters()
                    interactive = self.master.get_interactive()
                    bs = self.master.get_bs()
                    self.view.show_parameters(parameters, interactive, bs)
                    continue
                elif command[0] == 'sweep':
                    self.master.add_sweep(int(command[1]), int(command[2]), int(command[3]), int(command[4]))
                    continue
                    # sweeps.append([command[1], command[2], command[3], command[4]])
                elif command[0] == 'execute':

                    # execute2(bs, interesting, interactive, sweeps, controller)
                    self.master.execute()
                    continue

                elif command[0] == 'print':
                    # print(bs)
                    # elif command[0] == 'reload':
                    #	imp.reload(datasweep)
                    self.master.close_file()
                elif command[0] == 'show':
                    # return
                    self.master.close_file()
                elif command[0] == 'exit':
                    self.master.close_file()
                    # if f is not None:
                    #     f.close()
                    #     print("Closed file %s" % filename)
                    quit(0)
        # finally:
        #     self.master.close_file()
        #     print("Derp")
        #     quit(7)
