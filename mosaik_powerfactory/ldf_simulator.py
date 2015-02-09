from mosaik_powerfactory import PowerFactorySimulator
import mosaik_api

class PowerFacotryLDFSimulator(PowerFactorySimulator):
    def __init__(self):
        """Constructor of the PowerFactorySimulator

        Creates an instance of the PowerFactoryLDFSimulation with the default
        option set. It also starts powerfactory in engine mode.

        Returns:
            A Instance of PowerFacotryLDFSimulator

        """
        # Init the super method
        super().__init__()

        # Set the default step sizes
        self.step_size = 900 #s

        # Set the LDF Options
        self.ldf_options = {
            "iopt_net" : 0,
        }

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
                ldf_options

        Returns:
            The meta dictionary of the simulator

        """
        super().init(sid,project_name,options)


        # Set the ldf options in the study case
        for attr, value in self.ldf_options.items():
            self.command.SetAttribute(attr,value)

        return self.meta #pylint: disable=E1101

    def _get_command(self):
        """Private method to get the requierd simulation object

        Returns:
            The powerfacotry.DataObejct with the commnad

        """
        self.command = self.pf.GetFromStudyCase("ComLdf")
        return self.command

    def _run_step(self,mosaik_time):
        """Private method to run a simulation step

        Updates the study case time to the new relative simulation time in
        mosaik and executes a load_flow calculation

        """
        # Set the time in the study case
        self._set_case_time(mosaik_time)
        #execute load flow
        self.command.Execute()



# Make it executable
def main():
    return mosaik_api.start_simulation(PowerFacotryLDFSimulator())


if __name__ == '__main__':
    main()
