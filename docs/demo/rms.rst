RMS-Simulation
==============

The minimal time step of MOSAIK is 1 s, which is usalay to high for RMS-
Simulation which requiere a timestep between <1ms to 100ms debending on the
modelled time constants. On the other hand for input date like load and generation
a time constant of 1 s is usually adequate. For types of input you can use
MOSAIK for PowerFacotry.

The PowerFactoryRMSSimulator has a internal time step size for the RMS-Simulation
itself and an external step size for the communication with MOSIAK. The exchange of
inpot data form MOSAIK to  PowerFactory is thereby realized by events. For each
step in the MOSAIK simulation the RMS-Simulater creates for each changing input value
of the modelles a parameter event and resume the RMS-Simulation until the end of the
MOSIAK time step.

The following code shows a simple RMS examble. It uses a PowerFactory Modell
to run a RMS simulation. Therby the active power of own load is controlled by
a CSV file. As Result the voltage of all terminals is printed.

.. literalinclude:: ../../demos/rms.py

To run this demo you should replace the projet_name with one project of your
PowerFactory database. The gird in this project schould have a least one load.
