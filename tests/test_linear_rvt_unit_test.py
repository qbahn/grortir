from unittest import TestCase
from unittest.mock import patch

import networkx as nx
import numpy as np

from grortir.main.model.processes.factories.calls_process_factory import \
    CallsProcessFactory
from grortir.main.optimizers.grouped_optimizer import GroupedOptimizer
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.calls_optimization_strategy import \
    CallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm


def prepare_rand_mock(rand_mock):
    """Rand mock for:
        3 particles
        5 stages
        2 dimensions
    """
    returned_values = [  # rand_vec - positions particle 1
        [0.0763, 0.7235],
        [0.5011, 0.4999],
        [0.3809, 0.9096],
        [0.9312, 0.9501],
        [0.9091, 0.7504],

        # rand_vec - initial_velocities particle 1
        [0.2048, 0.4774],
        [0.7686, 0.2760],
        [0.6574, 0.7193],
        [0.1805, 0.4265],
        [0.4149, 0.7094],

        # rand_vec - positions particle 2
        [0.7799, 0.9780],
        [0.0721, 0.6792],
        [0.0659, 0.2134],
        [0.0249, 0.2303],
        [0.1332, 0.6690],

        # rand_vec - initial_velocities particle 2
        [0.4908, 0.3659],
        [0.3140, 0.4528],
        [0.3704, 0.4130],
        [0.7411, 0.6344],
        [0.0014, 0.5243],

        # rand_vec - positions particle 3
        [0.4384, 0.5385],
        [0.2684, 0.8037],
        [0.2881, 0.4521],
        [0.6005, 0.5485],
        [0.5234, 0.4678],

        # rand_vec - initial_velocities particle 3
        [0.3724, 0.8379],
        [0.5726, 0.3530],
        [0.4591, 0.9064],
        [0.4224, 0.5229],
        [0.0923, 0.6962],

        # rand_1
        0.9555,
        # rand_2
        0.6829,
        # itd.
        0.0531,
        0.3089,
        0.5926,
        0.2351,
        0.9650,
        0.9450,
        0.8484,
        0.4723,
        0.8415,
        0.1311,
        0.3087,
        0.4630,
        0.7418,
        0.4858,
        0.1369,
        0.3435,
        0.3244,
        0.3004,
        0.1655,
        0.4149,
        0.4481,
        0.7749,
        0.7964,
        0.5224,
        0.4606,
        0.7782,
        0.8873,
        0.6749,
        0.8005,
        0.9391,
        0.0407,
        0.8757,
        0.2766,
        0.4758,
        0.7968,
        0.7172,
        0.1471,
        0.6587,
        0.0693,
        0.3571,
        0.8128,
        0.4277,
        0.5999,
        0.7282,
        0.8212,
        0.7605,
        0.0071,
        0.4203,
        0.4631,
        0.0555,
        0.5414,
        0.6078

    ]

    returned_values_arrays = []
    for row in returned_values:
        returned_values_arrays.append(np.array(row))

    rand_mock.side_effect = returned_values_arrays


class TestLinearRVT(TestCase):
    @patch('grortir.main.pso.velocity_calculator.np.random.rand')
    def test_RVT_mocked(self, rand_mock):
        """Test use some mocked values of random function from one known example from matlab.
         Because we set the same values in rand function, we should have equal values as in matlab.
         This is working example for 3 particles, 5 stages, 2 dimensions when all stages are in one group.
         """
        prepare_rand_mock(rand_mock)
        how_many_particles = 3
        calls_factory = CallsProcessFactory("linear", 5,
                                            1000,
                                            [0, 0])
        process = calls_factory.construct_process()

        ordered_stages = nx.topological_sort(process)

        # process = CallsProcess()
        # stage = CallsStage("stage_name", 1000, [0])
        # process.add_node(stage)
        # ordered_stages = [stage]

        grouping_strategy = GroupingStrategy(ordered_stages)
        grouping_strategy.define_group(ordered_stages)
        optimization_startegy = CallsOptimizationStrategy()

        pso_algortihm = PsoAlgorithm(process, grouping_strategy,
                                     optimization_startegy,
                                     how_many_particles)
        optimizer = GroupedOptimizer(process, grouping_strategy, pso_algortihm)

        optimizer.optimize_process()

        optimizer.result
