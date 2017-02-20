from unittest import TestCase
from unittest.mock import Mock

from grortir.main.pso.velocity_calculator import VelocityCalculator


class TestVelocityCalculator(TestCase):
    def test_calculate(self):
        stage = Mock()
        tested_object = VelocityCalculator()
        current_velocities = {stage: [0.5, 0.5]}
        particle_best_positions = {stage: [0.5, 0.5]}
        leader_best_positions = {stage: [0.5, 0.5]}
        control_params = {stage: [0.5, 0.5]}
        result = tested_object.calculate(current_velocities,
                                         particle_best_positions,
                                         leader_best_positions,
                                         control_params)
        self.assertIsInstance(result[stage], type([1, 2]))
        self.assertEquals(len(result), 1)
