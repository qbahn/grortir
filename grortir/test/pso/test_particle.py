from unittest import TestCase
from unittest.mock import Mock

import numpy as np

from grortir.main.pso.particle import Particle
from grortir.main.pso.position_updater import PositionUpdater
from grortir.main.pso.velocity_calculator import VelocityCalculator


class TestParticle(TestCase):
    def setUp(self):
        self.particle_mock = Mock()
        self.stages = [Mock(), Mock()]
        self.position_updaters = {stage: Mock() for stage in self.stages}
        self.velocity_calculator = Mock()
        for i in range(len(self.stages)):
            self.velocity_calculator.calculate_initial_velocity.return_value = 0.01 * (i + 1)
        self.particle_mock.stages = self.stages
        self.particle_mock.position_updaters = self.position_updaters
        self.particle_mock.velocity_calculator = self.velocity_calculator
        self.particle_mock.current_velocities = {}
        self.particle_mock.current_quality = {stage: 100 for stage in
                                              self.stages}
        self.process = Mock()
        self.particle_mock.process = self.process

    def test_get_the_overall_quality_po(self):
        particle_mock = Mock()
        particle_mock.current_quality = {'a': 2, 'b': 3, 'c': -3.1234}
        result = Particle.get_the_overall_quality(particle_mock)
        self.assertEqual(result, 3)

    def test___init__(self):
        particle = Particle(self.stages, self.process, 7)
        self.assertIsNotNone(particle)
        self.assertEqual(particle.best_quality, np.inf)

    def test__set_initial_positons(self):
        Particle._set_initial_positions(self.particle_mock)
        for stage in self.stages:
            self.position_updaters[
                stage].set_initial_control_params.assert_any_call()

    def test__set_initial_velocities(self):
        Particle._set_initial_velocities(self.particle_mock)
        i = 0
        for stage in self.stages:
            self.assertEqual(self.particle_mock.current_velocities[stage],
                             0.01 * (i + 1))
            i += 1

    def test_initialize(self):
        Particle.initialize(self.particle_mock)
        for stage in self.stages:
            self.assertEqual(self.particle_mock.position_updaters[stage].stage,
                             stage)
            self.assertIsInstance(self.particle_mock.position_updaters[stage],
                                  PositionUpdater)
            self.assertEqual(
                self.particle_mock.velocity_calculators[stage].stage,
                stage)
            self.assertIsInstance(
                self.particle_mock.velocity_calculators[stage],
                VelocityCalculator)
        self.particle_mock._set_initial_positions.assart_any_call()
        self.particle_mock._set_initial_velocities.assart_any_call()

    def test_update_values(self):
        Particle.update_values(self.particle_mock)
        self.particle_mock.update_input_vectors.assert_any_call()
        self.particle_mock.calculate_current_quality.assert_any_call()
        self.particle_mock._update_best_position.assert_any_call()
