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
        "num_elements_of_model"
    ],
}

class PowerFacotyCommands(Enum):
    CmdLdf = 1
    CmdRms = 2


class PowerFactorySimulator(mosaik_api.Simulator):
    def __init__(self):
        # Init the Metadata in the Super Class
        super().__init__(META)
        # Init Power Facotry
        self.pf = powerfactory.GetApplication()
        if self.pf is None:
            raise Exception("Starting PowerFactory application in engine mode failed")

        # Set the default simulation method
        self.command = PowerFacotyCommands.CmdLdf

        # Set the default step sizes
        self.step_size = 1 #s
        self.rms_step_size = 0.01 #s internal rms step size

        # Create the entities Container
        self.entities = {}  # Maps EIDs to model indices in PowerFactory

    def init(self, sid, project_name , command = PowerFacotyCommands.CmdLdf, step_size = 1, rms_step_size = 0.01):

        # Option overwrite the command
        if command is not None:
            self.command = command

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

    def num_elements_of_model(self, model, name="*"):
        return len(self.elements_of_model(model, name))




# Make it executable
def main():
    return mosaik_api.start_simulation(PowerFactorySimulator())


if __name__ == '__main__':
    main()
