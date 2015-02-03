# mosaik-powerfacoty.py
"""
Mosaik interface for Digisilent Powerfactory

"""
import sys
import os
os.environ["PATH"] = "C:\\Program Files\\DIgSILENT\\PowerFactory 15.2;" + os.environ["PATH"]
sys.path.append("C:\\Program Files\\DIgSILENT\\PowerFactory 15.2\\python\\3.4")
import powerfactory

import mosaik_api
import arrow
from dateutil import tz
import abc

META = {
    'api_version': '2.1.2',
    'models': {
        'ElmLod' : {
            'public': True,
            'params': ['loc_name'],
            'attrs': ['plini'],
        },
    },
    'extra_methods': [
        "elements_of_model",
        "num_elements_of_model",
        "element_with_eid",
    ],
}

class PowerFactorySimulator(mosaik_api.Simulator):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        # Init the Metadata in the Super Class
        super().__init__(META)
        # Init Power Facotry
        self.pf = powerfactory.GetApplication()
        if self.pf is None:
            raise Exception("Starting PowerFactory application in engine mode failed")

        # Set the default step sizes
        self.step_size = 1 #s

        # Set the default referenze time
        self.ref_date_time = arrow.Arrow(2014,1,1,0,0,0,tzinfo=tz.tzlocal())

        # Set the studdy case to none by default
        self.study_case = None

        # Set the command object to none as default
        self.command = None

    #def init(self, sid, project_name , step_size = None, study_case = None, ref_date_time = None):
    def init(self, sid, project_name , options = None):
        del sid

        # Set the Simulation Options
        if options is not None:
            for attr,value in options.items():
                if value is not None:
                    setattr(self,attr,value)

        # Activate project in powerfactory
        if project_name is None:
            raise Exception("You have to provide the project_name for PowerFactory")
        self.pf.ActivateProject(project_name)

        # Activate the study cae
        if self.study_case is None:
            # If there is no study_case given get the current study case
            case = self.pf.GetActiveStudyCase()
            self.study_case = case.loc_name
        else:
            cases = self.pf.GetProjectFolder('study').GetChildren(0,'%s.IntCase' % self.study_case)[0]
            if cases is None:
                raise Exception("There is no study case with the name %s in your PowerFactory project" % self.study_case)
            else:
                case = cases[0]
                case.Activate()

        # Set the ref_date_time to the study case
        self._set_case_time(0)

        # Get the calculation commend
        self._get_command()



        # this methode has to return the meta dict
        return self.meta #pylint: disable=E1101


    def elements_of_model(self, model, name="*"):
        if self.pf.GetActiveProject is None:
            raise Exception("You have to init the simulator first")
        return self.pf.GetCalcRelevantObjects('%s.%s' % (name, model),1,1)

    def element_with_eid(self,eid):
        if self.pf.GetActiveProject is None:
            raise Exception("You have to init the simulator first")
        element =  self.pf.GetCalcRelevantObjects(eid,1,1)
        if not element:
            raise Exception("No element with eid: %s" % eid)
        if len(element) > 1:
            raise Exception("Found more of one element with eid: %s" % eid)

        return element[0]


    def num_elements_of_model(self, model, name="*"):
        return len(self.elements_of_model(model, name))


    def create(self, num, model, loc_name):

        entities = []

        # Get the elements name from powerfactory
        elements = self.elements_of_model(model,loc_name)

        # Errors:
        if elements is None:
            raise Exception("There is no model with the name %s.%s in your PowerFactory Model" % (loc_name,model))

        if num != len(elements):
            raise Exception("The number of models have to be the equal the models in your PowerFactor Model")

        # Mapping Elements for Mosaik
        for e in elements:
            eid = '%s.%s' % (e.loc_name, model)
            entities.append({'eid': eid, 'type': model})

        return entities


    def step(self, mosaik_time, inputs):
        # Input could look like this
        # {
        #     'Load1.ElmLod': {
        #         'plini': {'src_eid_0': 1},
        #     },
        #     'Load2.ElmLod':
        #         'plini': {'src_eid_1': 2},
        #     },
        # }
        for eid, attrs in inputs.items():

            # Get PF element
            element = self.element_with_eid(eid)

            # Set the attribes of the elements
            for attr, sources in attrs.items():
                new_value = sum(sources.values()) # We not care about the sources
                element.SetAttribute(attr,new_value)

        self._run_step(mosaik_time)

        #When we want to do the next simulation step
        return mosaik_time + self.step_size

    def get_data(self, outputs):
        # The outputs parameter can look like this
        # {
        #     'Load1.ElmLod': ['plini'],
        #     'Load2.ElmLod': ['plini'],
        # }

        # Init the data dictonary
        data = {}
        # Loop over the entity id for requested data
        for eid, attrs in outputs.items():
            # Get the element from the eid
            element = self.element_with_eid(eid)
            data[eid] = {}
            # Loop over the requested attributes
            for attr in attrs:
                # Get the attribute of the element
                data[eid][attr] = element.GetAttribute(attr)

        return data

    def _set_case_time(self,mosaik_time):
        # Get the study case
        case = self.pf.GetActiveStudyCase()
        # Calculate the resulting date
        dt = self.ref_date_time.replace(seconds=+mosaik_time)
        # set the time with the unix time stamp
        case.SetStudyTime(dt.float_timestamp)


    @abc.abstractmethod
    def _run_step(self,mosaik_time):
        return

    @abc.abstractmethod
    def _get_command(self):
        return


class PowerFacotryLDFSimulator(PowerFactorySimulator):
    def __init__(self):
        # Init the super method
        super().__init__()

        # Set the default step sizes
        self.step_size = 900 #s

        # Set the LDF Options
        self.ldf_options = {
            "iopt_net" : 0,
        }

    def init(self, sid, project_name , options = None): #pylint: disable=W0221
        super().init(sid,project_name,options)

        # Set the ldf options in the study case
        for attr, value in self.ldf_options.items():
            self.command.SetAttribute(attr,value)

        return self.meta #pylint: disable=E1101

    def _get_command(self):
        self.command = self.pf.GetFromStudyCase("ComLdf")
        return self.command

    def _run_step(self,mosaik_time):
        # Set the time in the study case
        self._set_case_time(mosaik_time)
        #execute load flow
        self.command.Execute()



# Make it executable
def main():
    return mosaik_api.start_simulation(PowerFacotryLDFSimulator())


if __name__ == '__main__':
    main()
