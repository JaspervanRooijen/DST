from View import *
from Master import *


class Controller:
    """
    The Controller is the connection which is made between a View and a Model, as expected in MVC-modeled software.
    The View is specified globally within the controller, as is the Master
    """
    view = None
    master = Master()

    def __init__(self):
        """
        The __init__ method initialises a View, as the controller must be given as argument to deal with user input.
        """
        self.view = GuiView(self)
        return

    def main(self, command):
        # Todo: Split
        """
        The main method is a method originally used as basis for a TUI, but is still used by the GUI for historic
        reasons. This method arranges Model changes accordingly based on user input in the View. Relatively new changes
        are not dealt with through this method, but separate smaller methods.

        This method should be splitted up in the future.

        E.g.
        > Controller.main('sweep 0 0 10 1')
        > None

        :param command: This is the command (as string) that is given to the method and describes the user input in a
        way that the Controller can forward it to the Model.
        :return: None
        """
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

    def get_sweeps(self):
        """
        Returns all sweeps that are stored in the model.
        :return: List of all currently stored sweeps.

        E.g.
        > Controller.get_sweeps()
        > [[0, 0, 10, 1], [1, 0, 20, 2]]
        """
        return self.master.get_sweeps()

    def quit(self):
        # Todo: Work out.
        """
        Called when the program is exited (both forced and unforced). Exits python.
        :return: quit(0)

        E.g.
        > Controller.quit()
        > quit()
        """
        print('Graceful exit!')
        quit(0)

    def simulate(self, amount, query):
        """
        Used for simulating an amount of runs, considering parameter query.
        :param amount: The amount of runs that should be carried out over the UPPAAL-model stored in the Model.
        :param query: The UPPAAL-parameter that should be considered.
        :return: A list of traces of every run taken.

        E.g.
        > simulate(2, 'cost')
        > [ [ (0,0), (1,1), (2,2) ], [ (0,0), (1,2), (2,2) ] ]
        """
        return self.master.simulate(amount, query)


c = Controller()
