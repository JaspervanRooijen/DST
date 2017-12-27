from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename


class TuiView:
    def loop(self, controller):
        while True:
            command = input('>').split(" ")
            controller.main(command)

    def show_parameters(self, parameters, interactive, bs):
        for par in parameters.keys():
            # if parameters[par] == "transition":
            #     source_id = par.source['ref']
            #     target_id = par.target['ref']
            #     source = ""
            #     target = ""
            #     prob = ""
            #     # print('sourceID: %s\ntargetID: %s\n' % (sourceID, targetID))
            #     for loc in bs.findAll('location'):
            #         if loc['id'] == source_id:
            #             if loc.find('name') is not None:
            #                 source = ' '.join(loc.find('name').contents)
            #             else:
            #                 source = 'Unnamed (id: %s)' % loc['id']
            #         if loc['id'] == target_id:
            #             # print('In the targetloc loop, %s' % loc)
            #             if loc.find('name') is not None:
            #                 target = ' '.join(loc.find('name').contents)
            #             else:
            #                 target = 'Unnamed (id: %s)' % loc['id']
            #     for label in par.findAll('label'):
            #         if label['kind'] is not None and label['kind'] == 'probability':
            #             prob = label.contents[0]
            #     if source == "":
            #         source = ('Branchpoint (id: %s)' % loc['id'])
            #     print("Transition %d:\n%s -> %s (Probability: %s)" % (interactive.index(par), source, target, prob))
            if parameters[par] == "declaration":
                print("Declaration %d\n%s" % (interactive.index(par), par))
            print("")


app = Flask(__name__)
gui = None

UPLOAD_FOLDER_creator = str(__file__).split('\\')
UPLOAD_FOLDER_creator[-1] = 'uploads'
UPLOAD_FOLDER = '\\'.join(UPLOAD_FOLDER_creator)

ALLOWED_EXTENSIONS = ['xml']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class GuiView:
    thread = None
    controller = None

    def __init__(self, controller):
        global gui
        gui = self
        self.controller = controller
        try:
            run()
        finally:
            self.controller.quit()

    def quit(self):
        self.thread.join()


def run():
    app.run()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global gui
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            gui.controller.main('openFile %s' % os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/data')
    return render_template('upload_file.html')


@app.route('/data', methods=['GET', ])
def add_sweep():
    global gui
    start = request.args.get('start', '')
    stop = request.args.get('stop', '')
    step = request.args.get('step', '')
    parameter = request.args.get('parameter', '')

    parameters, interactive, bs = gui.controller.main('parameters')

    # print('Start: %s\nStop: %s\nStep: %s\nParameter: %s' % (start, stop, step, parameter))
    if start != '' and stop != '' and step != '' and parameter != '':
        interactive_index = -1
        for index in interactive:
            # similar = True
            # print(index)

            if str(index) in parameter:
                interactive_index = interactive.index(parameter)
        if interactive_index != -1:
            gui.controller.main("sweep %s %s %s %s" % (interactive_index, start, stop, step))
        else:
            raise ValueError('Interactive_index could not be found: parameter unknown!')
    sweeps = gui.controller.get_sweeps()
    # print("Sweeps = " + str(sweeps))
    return render_template('parameters.html', parameters=interactive, sweeps=sweeps)


@app.route('/execute')
def execute():
    # print('Wow')
    result = gui.controller.main('execute')
    print(result)

    return render_template('results.html', data=json.dumps(result))


@app.route('/simulate')
def simulate():
    global gui
    amount = request.args.get('sims', '')
    query = request.args.get('query', '')
    result = gui.controller.simulate(amount, query)
    return "Enough for now"
