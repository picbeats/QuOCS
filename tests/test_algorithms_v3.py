import os
from scipy import optimize
import numpy as np

from quocs_optlib.communication.AllInOneCommunication import AllInOneCommunication
from quocs_optlib.figureofmeritevaluation.AbstractFom import AbstractFom
from quocs_optlib.handleexit.AbstractHandleExit import AbstractHandleExit
from quocs_optlib.tools.dynamicimport import dynamic_import
from quocs_optlib.tools.inputoutput import readjson


class FigureOfMerit(AbstractFom):
    def get_FoM(self, pulses, parameters, timegrids):
        return {"FoM": optimize.rosen(np.asarray(parameters))}


class HandleExit(AbstractHandleExit):
    pass


def main(optimization_dictionary: dict):
    # Initialize the communication object
    interface_job_name = optimization_dictionary["optimization_client_name"]
    communication_obj = AllInOneCommunication(interface_job_name=interface_job_name, fom_obj=FigureOfMerit(),
                                              handle_exit_obj=HandleExit())
    # Get the optimizer attribute
    optimizer_attribute = dynamic_import(
        attribute=optimization_dictionary.setdefault("opti_algorithm_attribute", None),
        module_name=optimization_dictionary.setdefault("opti_algorithm_module", None),
        class_name=optimization_dictionary.setdefault("opti_algorithm_class", None))
    # Create the optimizer object
    optimizer_obj = optimizer_attribute(optimization_dict=optimization_dictionary,
                                        communication_obj=communication_obj)
    print("The optimizer was initialized successfully")
    optimizer_obj.begin()
    print("The optimizer begin successfully")
    optimizer_obj.run()
    print("The optimizer run successfully")
    optimizer_obj.end()
    print("The optimizer end successfully")


if __name__ == '__main__':
    main(readjson(os.path.join(os.getcwd(), "algorithm_dictionary_v3.json"))[1])