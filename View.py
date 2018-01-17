from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename


class TuiView:
    """
    The class that was historically used as a Textual User Interface. Has not (yet) been updated to current Controller
    standards. Until update, this class is undocumented.
    """
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



"""
Basic initialisation for the GUI. A Flask application is initialised (but not started!). An upload folder is specified,
as well as allowed extensions.
"""
app = Flask(__name__)
gui = None

UPLOAD_FOLDER_creator = str(__file__).split('\\')
UPLOAD_FOLDER_creator[-1] = 'uploads'
UPLOAD_FOLDER = '\\'.join(UPLOAD_FOLDER_creator)

ALLOWED_EXTENSIONS = ['xml']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class GuiView:
    """
    Graphical Interface that is inferred by the Controller and handles all user input and output. Once started, most
    power of the Controller is outsourced to this class, in order to give the user full control over the application.
    In the end GuiView will always return to the Controller.
    """
    thread = None
    controller = None

    def __init__(self, controller):
        """
        Inferred by the Controller in order to start the GUI. The Controller object is stored within the class and the
        Flask application is started. After this, the class outsources the user input and output to the Flask
        application until it returns to the Controller.
        :param controller:
        """
        global gui
        gui = self
        self.controller = controller
        try:
            run()
        finally:
            self.controller.quit()

    # Todo: Check if this is used, otherwise: delete
    def quit(self):
        self.thread.join()


def run():
    """
    Starts the Flask application, which has been initialised earlier.
    :return: None
    """
    app.run()


def allowed_file(filename):
    """
    Checks if the uploaded file is allowed to be uploaded, as defined globally.
    :param filename: The filename of the file that is requested to be uploaded.
    :return: Boolean, file is either allowed to be uploaded, or not.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    The part of the Flask application situated at the root. Allows for the uploading of UPPAAL-models that can be used
    within the application afterwards. Only one UPPAAL-model at a time is allowed to be uploaded.
    :return: upload_file.html, containing the form for uploading files.
    """
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
    """
    The part of the Flask application that allows viewing all parameters detected within the UPPAAL system, adding
    parameter sweeps as well as start executing a data sweep or simulation.
    :return: parameters.html, updated with current information about parameters and sweeps in the Model.
    """
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
    """
    The part of the Flask application that shows the results of an executed data sweep over a parameter, as defined in
    the add_sweep-method.
    :return: results.html, updated with information retrieved from the execution of the data sweep.
    """
    # print('Wow')
    result = gui.controller.main('execute')
    print(result)

    return render_template('results.html', data=json.dumps(result))


@app.route('/simulate')
def simulate():
    """
    The part of the Flask application that shows the results of an executed simulation order, as defined in the
    add_sweep-method.
    :return: 
    """""
    global gui
    amount = request.args.get('sims', '')
    query = request.args.get('query', '')
    result = gui.controller.simulate(amount, query)
    # print(result)
    all_sets = {}
    for key in result.keys():
        datasets = []
        for data in result[key]:
            dataset = []
            data = data.split('(')
            for point in data:

                point = point.split(',')
                print(point)
                if len(point) == 2:
                    point[1].replace(')', '')
                    p = {}
                    # try:
                    p['x'] = int(point[0])
                    p['y'] = int(point[1])
                    # except ValueError:
                        # print('raaaah' + str(point))
                    dataset.append(p)
                else:
                    datasets.append(dataset)
                    dataset = []

        all_sets[key] = datasets
    # print(all_sets)
    return "Enough for now"
