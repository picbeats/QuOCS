# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright 2021-  QuOCS Team
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os, sys
import pytest
from quocslib.Controls import Controls
from quocslib.utils.inputoutput import readjson
import numpy as np


"""
Script to check controls initialization, basis vector (random super_parameters), getting sigma variation and
mean value for the start simplex generation.
"""


@pytest.fixture
def controls_obj():
    dir_of_this_file = sys.path[0]
    controls_dict = readjson(os.path.join(dir_of_this_file, "controls_dictionary.json"))[1]
    local_controls_obj = Controls(controls_dict["pulses"], controls_dict["times"], controls_dict["parameters"])
    local_controls_obj.select_basis()
    return local_controls_obj


def test_sigma_variation(controls_obj):
    desired_sigma_variation = np.array([0.08485281, 0.08485281, 0.08485281, 0.08485281, 0.5])
    difference = abs(desired_sigma_variation - controls_obj.get_sigma_variation())
    # check if the difference is smaller than 1e-8
    comparison = difference < 1e-8
    assert comparison.all()


def test_mean_value(controls_obj):
    desired_mean_value = np.array([0.0, 0.0, 0.0, 0.0, 0.01])
    difference = abs(desired_mean_value - controls_obj.get_mean_value())
    # check if the difference is smaller than 1e-8
    comparison = difference < 1e-8
    assert comparison.all()


def test_controls(controls_obj):
    controls_list = [pulses_list, time_grids_list, parameters_list] = \
                controls_obj.get_controls_lists(controls_obj.get_mean_value())
    # I dont know what this does
    controls_obj.update_base_controls(controls_obj.get_mean_value())
    # I don't know if it makes sense to compare anything here to some predefines values
    # let's just return true, so if the code runs without errors we pass the test... is this something
    # one should do?
    return True


# def main(controls_dict):
#     # Initialize controls
#     controls_obj = Controls(controls_dict["pulses"], controls_dict["times"], controls_dict["parameters"])
#     # Set random super_parameters
#     controls_obj.select_basis()
#     # Sigma variation
#     print("sigma_variation = {0}".format(controls_obj.get_sigma_variation()))
#     # Mean value
#     print("mean_value = {0}".format(controls_obj.get_mean_value()))
#     # Get control lists
#     controls_list = [pulses_list, time_grids_list, parameters_list] = \
#         controls_obj.get_controls_lists(controls_obj.get_mean_value())
#     for control in controls_list:
#         print("Control: {0}".format(control))
#     controls_obj.update_base_controls(controls_obj.get_mean_value())
#     print("The initialization is concluded")
#
#
# if __name__ == '__main__':
#     main(readjson(os.path.join(os.getcwd(), "controls_dictionary.json"))[1])
