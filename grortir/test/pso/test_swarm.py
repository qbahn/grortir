from unittest import TestCase

import numpy as np
import unittest.mock as mo

from grortir.main.pso.swarm import Swarm


class TestSwarm(TestCase):
    def setUp(self):
        self.stages = mo.Mock()
        self.process = mo.Mock()
        self.number_of_particles = 40
        self.tested_object = Swarm(self.process, self.stages,
                                   self.number_of_particles)
        self.mock_of_swarm = mo.Mock()
        self.mock_of_particle_1 = mo.Mock()
        self.mock_of_particle_2 = mo.Mock()
        self.mock_of_swarm.particles = [self.mock_of_particle_1,
                                        self.mock_of_particle_2]
        self.mock_of_best_particle = mo.Mock()
        self.mock_of_swarm.best_particle = self.mock_of_best_particle

    def test_constructor(self):
        self.assertIsNotNone(self.tested_object)
        self.assertEqual(self.stages, self.tested_object.stages)
        self.assertEqual(self.tested_object.number_of_particles,
                         self.number_of_particles)

    def test_initialize(self):
        Swarm.initialize(self.mock_of_swarm)
        self.mock_of_particle_1.initialize.assert_any_call()
        self.mock_of_particle_2.initialize.assert_any_call()

    def test_do_single_iteration(self):
        self.mock_of_swarm.particles = [self.mock_of_particle_1,
                                        self.mock_of_particle_1]
        expected_calls_particle = [mo.call.update_values(),
                                   mo.call.update_values(),
                                   mo.call.move(), mo.call.move()]
        expected_calls_swarm = [mo.call._update_best_particle(),
                                mo.call._update_velocieties()]

        Swarm.do_single_iteration(self.mock_of_swarm)

        self.assertListEqual(expected_calls_particle,
                             self.mock_of_particle_1.method_calls)
        self.assertListEqual(expected_calls_swarm,
                             self.mock_of_swarm.method_calls)

    def test__update_best_particle_1(self):
        self.mock_of_swarm.best_particle_quality = np.inf
        self.mock_of_particle_1.best_quality = 7
        self.mock_of_particle_2.best_quality = 6

        Swarm._update_best_particle(self.mock_of_swarm)

        self.assertEqual(self.mock_of_swarm.best_particle_quality, 6)
        self.assertEqual(self.mock_of_swarm.best_particle,
                         self.mock_of_particle_2)

    def test__update_best_particle_2(self):
        self.mock_of_swarm.best_particle_quality = np.inf
        self.mock_of_particle_1.best_quality = 7
        self.mock_of_particle_2.best_quality = 8

        Swarm._update_best_particle(self.mock_of_swarm)

        self.assertEqual(self.mock_of_swarm.best_particle_quality, 7)
        self.assertEqual(self.mock_of_swarm.best_particle,
                         self.mock_of_particle_1)

    def test__update_velocieties(self):
        Swarm._update_velocieties(self.mock_of_swarm)
        self.mock_of_particle_1.update_velocities.assert_called_once_with(
            self.mock_of_best_particle)
        self.mock_of_particle_2.update_velocities.assert_called_once_with(
            self.mock_of_best_particle)
