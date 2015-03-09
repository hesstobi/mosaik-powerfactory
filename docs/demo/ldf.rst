Load-Flow-Simulation
====================

The following code shows a simple load flow examble. It uses a PowerFactory Modell
to run a load flow simulation. Therby the active power of own load is controlled by
a CSV file. As Result the voltage of all terminals is printed.

.. literalinclude:: ../../demos/ldf.py


To run this demo you should replace the projet_name with one project of your
PowerFactory database. The gird in this project schould have a least one load.
