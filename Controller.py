from View import *
from Master import *


class Controller:
    view = None
    master = Master()

    def __init__(self):
        print('hello')
        self.main('openFile OctTWES.xml')
        print('success')
        self.view = GuiView(self)
        return

    def main(self, command):
        command = command.split(" ")
        if command[0] == 'openFile':
            print('hello2')
            if self.master.open_file(command[1]):
                print('File %s opened' % command[1])
            else:
                print('Filename unknown, failed opening...')
        elif command[0] == 'parameters':
            parameters = self.master.get_parameters()
            interactive = self.master.get_interactive()
            bs = self.master.get_bs()
            # print(str(parameters) + '\n\n')
            # print(str(interactive) + '\n\n')
            # print(bs)
            return parameters, interactive, bs
        elif command[0] == 'sweep':
            self.master.add_sweep(int(command[1]), int(command[2]), int(command[3]), int(command[4]))
            # sweeps.append([command[1], command[2], command[3], command[4]])
        elif command[0] == 'execute':
            return self.master.execute()
        elif command[0] == 'show':
            self.master.close_file()
        elif command[0] == 'exit':
            self.master.close_file()


c = Controller()
