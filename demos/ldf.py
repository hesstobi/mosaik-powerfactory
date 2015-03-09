import mosaik
import mosaik.util

import mosaik_csv
import mosaik_powerfactory

# Define the Simulator Configuration
SIM_CONFIG = {
    'PFSim': {
        #'python': 'mosaik_powerfactory:PowerFactoryLDFSimulator'
        'cmd': 'mosaik-powerfactory-ldf %(addr)s',
    },
    'Collector': {
        'cmd': 'python collector.py %(addr)s',
    },
     'CSV': {
        'python': 'mosaik_csv:CSV',
    },
}

START = '2014-01-01 00:00:00'
END = 1 * 24 * 3600  # 1 day
HH_DATA = 'data/household.csv'

# Create World, increase timeout for power-factory
world = mosaik.World(SIM_CONFIG,{'start_timeout':60})

# Start simulators and get the model factory
pfsim = world.start('PFSim', project_name='MOSIAK\\DEV', options={'ref_date_time': START})
hhsim = world.start('CSV', sim_start=START, datafile=HH_DATA, delimiter=';')
collector = world.start('Collector', step_size=900)

# Instantiate models using the model factory
Netz = pfsim.ElmNet(loc_name='Netz')
monitor = collector.Monitor()
load_input = hhsim.Household.create(1)[0]

# Access the powerfactory entities
loads = Netz.children_of_model('ElmLod')
Last1 = loads[0] # or: Last1 = Netz.child_with_eid('Netz\\Last1.ElmLod')
terminals = Netz.children_of_model('ElmTerm')

# Connect entities
world.connect(load_input,Last1,("P","e:plini"))
mosaik.util.connect_many_to_one(world,terminals, monitor, 'm:Ul')


# Run simulation
world.run(until=END)
