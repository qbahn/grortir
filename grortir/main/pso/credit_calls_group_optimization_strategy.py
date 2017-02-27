# pylint: disable=redefined-variable-type
import numpy as np

from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.pso.group_optimization_strategy import \
    GroupOptimizationStrategy


class CreditCallsGroupOptimizationStrategy(GroupOptimizationStrategy):
    """Optimization with credits.
        Attributes:
            stages_in_group (list): stages in group
            process (AbstractProcess): optimized process
            max_calls_for_group (int): max calls which can be
                used for this group
            expected_quality (float): expected quality
    """

    def __init__(self, stages_in_group, process):
        self.stages_in_group = stages_in_group
        self.process = process
        self.max_calls_for_group = 0
        self.expected_quality = np.inf

    def initialize(self):
        """
            Called once and set initial value of max_calls_for_group.
        """
        if self._calculate_current_cost_in_group() != 0:
            raise ValueError(
                "Stages in group shouldn't started with initial cost.")
        all_initial_calls = 0
        already_used_calls = 0
        all_stages = self.process.nodes()
        for stage in all_stages:
            all_initial_calls += stage.get_maximal_acceptable_cost()
        for stage in all_stages:
            already_used_calls += stage.get_cost()
        self.max_calls_for_group = all_initial_calls - already_used_calls

        for stage in self.stages_in_group:
            if self.expected_quality > stage.maximum_acceptable_quality:
                self.expected_quality = stage.maximum_acceptable_quality

    def should_continue(self, best_particle):
        """
        Return true if optimization should be continued for Calls Process with
        credits.
        Args:
            best_particle Particle: best particle in swarm.

        Returns:
            bool: true if continuation is required.

        """
        return self._is_safe_cost() and not self._is_enough_quality(
            best_particle)

    def finalize(self, best_particle):
        """
        Set proper status after finished group optimization.
        Args:
            best_particle (Particle): best particle in Swarm
        """
        optimizatin_status = OptimizationStatus.failed
        if self._is_safe_cost() and self._is_enough_quality(
                best_particle):
            optimizatin_status = OptimizationStatus.success
        for stage in self.stages_in_group:
            stage.optimization_status = optimizatin_status

    def _is_safe_cost(self):
        return (
            self._calculate_current_cost_in_group() <= self.max_calls_for_group)

    def _is_enough_quality(self, best_particle):
        return best_particle.best_quality <= self.expected_quality

    def _calculate_current_cost_in_group(self):
        calls_used_in_group = 0
        for stage in self.stages_in_group:
            calls_used_in_group += stage.get_cost()
        return calls_used_in_group
