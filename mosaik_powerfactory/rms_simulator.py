from .simulator import PowerFactorySimulator

import mosaik_api
import mosaik.exceptions
import logging

logger = logging.getLogger('powerfactory.mosaik')

class PowerFactoryRMSSimulator(PowerFactorySimulator):
    def __init__(self):
        """Constructor of the PowerFactoryRMSSimulator

        Creates an instance of the PowerFactoryRMSSimulation with the default
        option set. It also starts powerfactory in engine mode.

        Returns:
            A Instance of PowerFacotryRMSSimulator

        """
        # Init the super method
        super().__init__()

        # Set the default step sizes
        self.step_size = 1 #s

        # Default RMS Options
        self.sim_options = {
            "iopt_sim" : "rms",
            "ipot_net" : "sym",
            "dtgrd" : 0.01,
            "dtout" : 0.01,
            "tstart": 0,
        }

        # Default LDF Options
        self.ldf_options = {
            "iopt_net" : 0,
        }

        # Init the Inc Command, will be set by the _get_command method
        self._inc_command = None
        # Init the LDF command, will be set by the _get_command method
        self._ldf_command = None

        # Init the Events Object
        self._events = None

    @property
    def sim_step_size(self):
        return self.sim_options.get("dtgrd",float('nan'))

    @sim_step_size.setter
    def sim_step_size(self,value):
        self.sim_options["dtgrd"]=value
        self.sim_options["dtout"]=value

    def init(self, sid, project_name , options = None): #pylint: disable=W0221
        """ Init method for the Mosaik interface

        Activates the given project and set the options to the simulator and the
        command

        Args:
            sid: The simulator sid
            project_name: The name of the PowerFactory project which the
                simulator should use
            options: A dictionary of optional options for the simulator.
                Possible keys are: step_size, ref_date_time, study_case,
                sim_options

        Returns:
            The meta dictionary of the simulator

        """
        super().init(sid,project_name,options)

        # Set the  inc options in the study case
        for attr, value in self.sim_options.items():
            self._inc_command.SetAttribute(attr,value)

        # Set the ldf options in the study case
        for attr, value in self.ldf_options.items():
            self._ldf_command.SetAttribute(attr,value)

        logger.debug('RMS Simulation will be calculated for %d seconds with a internal step size of %d seconds',self.step_size,self.sim_step_size)

        result = self._inc_command.Execute()
        if result is not 0:
            logger.error('Calculation %s failed',self._command.loc_name)
            raise mosaik.exceptions.SimulationError("Calculation of initial values failed")

        # Get the event object end delete old mosaik events
        self._events = self.pf.GetFromStudyCase("IntEvt")
        mosaik_events = self._events.GetChildren(0,'mosaik*')[0]
        for event in mosaik_events:
            event.Delete()


        return self.meta #pylint: disable=E1101

    def _get_command(self):
        """Private method to get the requierd simulation object

        For the RMS Simulation it gets the IncCom and the SimCom Objects from
        the study case.

        Returns:
            The powerfacotry.DataObejct with the command

        """
        self._command = self.pf.GetFromStudyCase("ComSim")
        self._inc_command = self.pf.GetFromStudyCase("ComInc")
        self._ldf_command = self.pf.GetFromStudyCase("ComLdf")
        return self._command


    def step(self, mosaik_time, inputs):
        """ rms step methods for the mosiak api

        It will set the inputs to the entities by creating a simulation event
        And run a rms simulation until the end of the step

        Args:
            mosaik_time: The relative simulation time in secounds
            inputs: The inputs to the elements

        Returns:
            The next relative simulation time

        """

        for eid, attrs in inputs.items():

            # Get PF element
            element = self.pf.element_with_unique_name(eid)

            # Set the attribes of the elements
            for attr, sources in attrs.items():
                new_value = sum(sources.values()) # We not care about the sources
                event = self._events.CreateObject('EvtParam','mosaik')[0]
                event.SetAttribute('p_target',element)
                event.SetAttribute('hrtime',0)
                event.SetAttribute('mtime',0)
                event.SetAttribute('time',mosaik_time)
                event.SetAttribute('variable',attr)
                event.SetAttribute('value',str(new_value))
                event.Execute()

        self._run_step(mosaik_time)

        #When we want to do the next simulation step
        return mosaik_time + self.step_size



    def _run_step(self,mosaik_time):
        """Private method to run a simulation step

        This method sets a new stop time for the rms simulation and runs then the
        simulation.

        """
        self._set_sim_stop_time(mosaik_time)
        result = self._command.Execute()
        if result is not 0:
            logger.error('Calculation %s failed',self._command.loc_name)
            raise mosaik.exceptions.SimulationError("RMS simulation failed")




    def _set_sim_stop_time(self,mosaik_time):
        """ Private method to set the simulatio stop time.

        This method set the simulation stop time, which is the time when the
        rms simulation should interrupt to get new data from mosaik. The stop time
        is set to the current mosaik_time+step_size.

        Args:
            mosaik_time: the current relative simualation time

        Returns:
            None

        """
        self._command.tstop = mosaik_time+self.step_size


# Make it executable
def main():
    return mosaik_api.start_simulation(PowerFactoryRMSSimulator())
