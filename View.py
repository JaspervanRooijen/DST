from flask import Flask, render_template, request
import json


class TuiView:
    def loop(self, controller):
        while True:
            command = input('>').split(" ")
            controller.main(command)

    def show_parameters(self, parameters, interactive, bs):
        for par in parameters.keys():
            if parameters[par] == "transition":
                source_id = par.source['ref']
                target_id = par.target['ref']
                source = ""
                target = ""
                prob = ""
                # print('sourceID: %s\ntargetID: %s\n' % (sourceID, targetID))
                for loc in bs.findAll('location'):
                    if loc['id'] == source_id:
                        if loc.find('name') is not None:
                            source = ' '.join(loc.find('name').contents)
                        else:
                            source = 'Unnamed (id: %s)' % loc['id']
                    if loc['id'] == target_id:
                        # print('In the targetloc loop, %s' % loc)
                        if loc.find('name') is not None:
                            target = ' '.join(loc.find('name').contents)
                        else:
                            target = 'Unnamed (id: %s)' % loc['id']
                for label in par.findAll('label'):
                    if label['kind'] is not None and label['kind'] == 'probability':
                        prob = label.contents[0]
                if source == "":
                    source = ('Branchpoint (id: %s)' % loc['id'])
                print("Transition %d:\n%s -> %s (Probability: %s)" % (interactive.index(par), source, target, prob))
            elif parameters[par] == "declaration":
                print("Declaration %d\n%s" % (interactive.index(par), par))
            print("")


app = Flask(__name__)
gui = None


class GuiView:
    thread = None
    controller = None

    def __init__(self, controller):
        global gui
        gui = self
        self.controller = controller
        run()

    def quit(self):
        self.thread.join()


def run():
    app.run()


@app.route('/')
def hello_world():
    return 'Hello World!'


# @app.route('/data')
# def show_data():
#     parameters, interactive, bs = gui.controller.main('parameters')
#     print(parameters)
#     print(interactive)
#     return render_template('parameters.html', parameters=interactive)


@app.route('/data', methods=['GET', ])
def add_sweep():
    start = request.args.get('start', '')
    stop = request.args.get('stop', '')
    step = request.args.get('step', '')
    parameter = request.args.get('parameter', '')

    parameters, interactive, bs = gui.controller.main('parameters')

    if start != '' and stop != '' and step != '' and parameter != '':
        # print(parameter)
        # print("")
        # print(interactive[0])
        # print("")
        # print(str(str(interactive[0])==(str(parameter))))
        interactive_index = -1
        for index in interactive:
            # similar = True
            print(index)

            if str(index) in parameter:
                interactive_index = interactive.index(parameter)

            # if parameters[index] == 'transition':
            #     for line in str(index):
            #         # print(line)
            #         # print(str(line in str(parameters)))
            #         if line not in str(parameter):
            #             similar = False
            # else:
            #     if index not in parameter:
            #         print(index)
            #         print(parameter)
            #         similar = False
            # if similar:
            #     interactive_index = interactive.index(index)
            # break
        # print('interactive_index = ' + str(interactive_index))
        # print(interactive[interactive_index])
        # interactive_index = interactive.index(parameter)
        gui.controller.main("sweep %s %s %s %s" % (interactive_index, start, stop, step))
    return render_template('parameters.html', parameters=interactive)


@app.route('/execute')
def execute():
    print('Wow')
    result = gui.controller.main('execute')
    print(result)

    return render_template('results.html', data=json.dumps(result))
