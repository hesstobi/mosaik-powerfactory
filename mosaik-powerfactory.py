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

META = {
    'api_version': '2.1.2',
    'models': {
        'ElmLod' : {
            'public': True,
            'params': ['loc_name'],
            'attrs': ['plini'],
        },
    },
}


class PowerFactorySimulator(mosaik_api.Simulator):
    def __init__(self):
        # Init the Metadata in the Super Class
        super().__init__(META)
        # Init Power Facotry
        self.pf = powerfactory.GetApplication()
        if self.pf is None:
            raise Exception("Starting PowerFactory application in engine mode failed")

        # Set a eid_prefix
        self.eid_prefix= 'PF_'

        # Create the entities Container
        self.entities = {}  # Maps EIDs to model indices in PowerFactory

    def init(self, sid, project_name ,eid_prefix=None):
        # Option overwrite the eid_prefix
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        # Activate project in powerfactory
        if project_name is None:
            raise Exception("You have to provide the project_name for PowerFactory")
        self.pf.ActivateProject(project_name)
        # this methode has to return the meta dict
        return self.meta





# Make it executable
def main():
    return mosaik_api.start_simulation(PowerFactorySimulator())


if __name__ == '__main__':
    main()
