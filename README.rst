Mosaik-Powerfactory
===================

Mosaik-Powerfactory provides an interface for `Mosaik`__
co-simulation framework.

__ https://mosaik.offis.de/

Installation
------------

Mosaik-Powerfactory requires Python >= 3.3. Use `pip`__ to install it,
preferably into a `virtualenv`__

.. code-block:: bash

    pip install -e git+https://gitlab.evieeh.local/tobias.hess/mosaik-powerfactory.git#egg=mosaik-powerfacotry


__ http://pip.readthedocs.org/en/latest/installing.html
__ http://virtualenv.readthedocs.org/en/latest/


Quickstart
----------

This is small example how tho use mosiak-powerfacotory to run a load flow
simulation with mosaik.

.. code-block:: python

    import mosiak_powerfacotry
    import mosaik

    SIM_CONFIG = {
       'PFSim': { 'python': 'mosaik_powerfactory:PowerFactoryLDFSimulator' }
    }
    world = mosaik.world(SIM-CONFIG)
    pfsim = world.start('PFSim', project_name='PROJECTNAME',options={})
    Netz = pfsim.ElmNet(loc_name='Netz')
    world.run(unit=1800)

The main steps to use PowerFactory with mosaik are:

1. Add the desired Powerfactory Simulator to your simulation config. Avaible
   simulators are:

  * **PowerFactoryLDFSimulator**: Load flow simulations
  * **PowerFactoryRMSSimulator**: RMS simulations

  You can use the simulator as python module or as cmd:

  * ``'python': 'mosaik_powerfactory:PowerFactoryLDFSimulator'``
  * ``'cmd': 'mosaik-powerfactory-ldf %(addr)s'``

2. Start the simulator with world.start which cals the init method of the
   simulator: :py:meth:`mosaik_powerfactory.PowerFactoryLDFSimulator.init` or
   :py:meth:`mosaik_powerfactory.PowerFactoryRMSSimulator.init`. Define the
   desierd project in the attribute :py:attr:`project_name`

3. Connect your PowerFoctory ``ElmNet`` with mosaik by creating it with its
   ``loc_name``, e.g: ``pfsim.ElmNet(loc_name='Netz')``

4. Connecting Grid elements with other simulators in mosaik. To get the desierd
   elements you can use this methods:

  * ``Last = Netz.child_with_eid('Netz\\Last1.ElmLod')``: get the element with the
    given Path
  * ``terminals = Netz.children_of_model('ElmTerm')``: get the elements of the
    given model

5. Run the simulation!

A detailed documentation of mosaik is avaible here: `Mosiak documentation`__.

__ http://mosaik.readthedocs.org/en/stable/

Documentation
-------------

To read the full documentation of this project follow these steps:

.. code-block:: bash

    git clone https://gitlab.evieeh.local/tobias.hess/mosaik-powerfactory.git
    cd mosaik-powerfactory/docs
    make html

Open the file :file:`.\_build\html\index.html` in your browser
