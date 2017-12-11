

class TuiView:
    def show_parameters(self, parameters, interactive, bs):
        for par in parameters.keys():
            if parameters[par] == "transition":
                sourceID = par.source['ref']
                targetID = par.target['ref']
                source = ""
                target = ""
                prob = ""
                # print('sourceID: %s\ntargetID: %s\n' % (sourceID, targetID))
                for loc in bs.findAll('location'):
                    if loc['id'] == sourceID:
                        if loc.find('name') is not None:
                            source = ' '.join(loc.find('name').contents)
                        else:
                            source = 'Unnamed (id: %s)' % loc['id']
                    if loc['id'] == targetID:
                        # print('In the targetloc loop, %s' % loc)
                        if loc.find('name') is not None:
                            target = ' '.join(loc.find('name').contents)
                        else:
                            target = 'Unnamed (id: %s)' % loc['id']
                for label in par.findAll('label'):
                    if label['kind'] is not None and label['kind'] == 'probability':
                        prob = label.contents[0]
                if (source == ""):
                    source = ('Branchpoint (id: %s)' % loc['id'])
                print("Transition %d:\n%s -> %s (Probability: %s)" % (interactive.index(par), source, target, prob))
            elif parameters[par] == "declaration":
                print("Declaration %d\n%s" % (interactive.index(par), par))
            print("")

