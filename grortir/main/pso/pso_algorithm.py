"""Contain PsoAlgorithm."""
# pylint: disable=redefined-variable-type
import logging

from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.pso.process_validator import ProcessValidator
from grortir.main.pso.whole_group_pso import WholeGroupPso

LOG = logging.getLogger(__name__)


class PsoAlgorithm:
    """Optimize process with different strategies.

    Attributes:
        process (AbstractProcess): process
        """

    def __init__(self, process, grouping_strategy, optimization_startegy,
                 number_of_particle=40):
        self.process = process
        self.grouping_strategy = grouping_strategy
        self.optimization_strategy = optimization_startegy
        self.process_validator = ProcessValidator()
        self.whole_group_pso = WholeGroupPso(self.process, number_of_particle)

    def run(self):
        """Run algorithm."""
        self.process_validator.validate(self.process)
        self.process.optimizationStatus = OptimizationStatus.in_progress
        number_of_groups = self.grouping_strategy.get_actual_numbers_of_groups()
        for current_group_number in range(number_of_groups):
            current_stages = self.grouping_strategy.get_items_from_group(
                current_group_number)
            group_optimization_strategy = self.optimization_strategy. \
                get_group_optimization_strategy(current_stages, self.process)
            self.whole_group_pso.optimize(current_stages,
                                          group_optimization_strategy)
        self._post_processing()

    def _post_processing(self):
        final_status = OptimizationStatus.success
        for stage in self.grouping_strategy.ordered_stages:
            if stage.optimization_status != OptimizationStatus.success:
                final_status = OptimizationStatus.failed
        self.process.optimization_status = final_status
        LOG.info('Final status of process optimization: ' + str(final_status))
