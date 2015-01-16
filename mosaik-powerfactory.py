# mosaik-powerfacoty.py
"""
Mosaik interface for Digisilent Powerfactory

"""
import sys
import os
os.environ["PATH"] = "C:\\Program Files\\DIgSILENT\\PowerFactory 15.2;" + os.environ["PATH"]
sys.path.append("C:\\Program Files\\DIgSILENT\\PowerFactory 15.2\\python\\3.4")
import powerfactory as pf

import mosaik_api

META = {
    'models': {
        'ElmLod' : {
            'public': True,
            'params': ['loc_name'],
            'attrs': ['plini'],
        },
    },
}


class PowerFactorySimulator(mosaik_api.Simulator)









# Make it executable
def main():
    return mosaik_api.start_simulation(ExampleSim())


if __name__ == '__main__':
    main()
