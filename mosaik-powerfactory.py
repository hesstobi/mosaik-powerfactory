# mosaik-powerfacoty.py
"""
Mosaik interface for Digisilent Powerfactory

"""
from enum import Enum

import sys
import os
os.environ["PATH"] = "C:\\Program Files\\DIgSILENT\\PowerFactory 15.2;" + os.environ["PATH"]
sys.path.append("C:\\Program Files\\DIgSILENT\\PowerFactory 15.2\\python\\3.4")
import powerfactory

import mosaik_api

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

class PowerFactoryCommands(Enum):
    balancedLoadFlow = 1
    unbalancedLoadFlow = 2
    rmsSimulation = 3
    emtSimulation = 4


class PowerFactorySimulator(mosaik_api.Simulator):
    def __init__(self):
        # Init the Metadata in the Super Class
        super().__init__(META)
        # Init Power Facotry
        self.pf = powerfactory.GetApplication()
        if self.pf is None:
            raise Exception("Starting PowerFactory application in engine mode failed")

        # Set the default simulation method
        self.command = PowerFactoryCommands.balancedLoadFlow

        # Set the default step sizes
        self.ldf_step_size = 900 #s
        self.rms_step_size = 1 #s
        self.rms_sim_step_size = 0.01 #s internal rms step size

        # Set the default referenze time
        self.ref_date_time = arrow.Arrow(2014,1,1,0,0,0,tzinfo=tz.tzlocal())

        # Set the studdy case to none by default
        self.study_case = None

        # Create the entities Container
        self.entities = {}  # Maps EIDs to model indices in PowerFactory

    def init(self, sid, project_name , command = PowerFactoryCommands.balancedLoadFlow, ldf_step_size = 900, rms_step_size = 1, rms_sim_step_size = 0.01, study_case = None, ref_date_time =arrow.Arrow(2014,1,1,0,0,0,tzinfo=tz.tzlocal())):

        # Option overwrite the command
        if command is not None:
            self.command = command

        # Option for simulation times
        if ldf_step_size is not None:
            self.ldf_step_size = ldf_step_size
        if rms_step_size is not None:
            self.rms_step_size = rms_step_size
        if rms_sim_step_size is not None:
            self.rms_sim_step_size = rms_sim_step_size

        # Option overwrite study_case
        if study_case is not None:
            self.study_case = study_case

        # Option overwrite ref_date_time
        if ref_date_time is not None:
            self.ref_date_time = ref_date_time

        # Activate project in powerfactory
        if project_name is None:
            raise Exception("You have to provide the project_name for PowerFactory")
        self.pf.ActivateProject(project_name)
        # this methode has to return the meta dict
        return self.meta


    def elements_of_model(self, model, name="*"):
        if self.pf.project is None:
            raise Exception("You have to init the simulator first")
        return self.pf.GetCalcRelevantObjects('%s.%s' % (name, model),1,1)

    def element_with_eid(self,eid):
        if self.pf.project is None:
            raise Exception("You have to init the simulator first")
        element =  self.pf.GetCalcRelevantObjects(eid,1,1)
        if element is empty:
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











# Make it executable
def main():
    return mosaik_api.start_simulation(PowerFactorySimulator())


if __name__ == '__main__':
    main()
