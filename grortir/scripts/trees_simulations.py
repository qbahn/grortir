import logging

from grortir.main.logging.logging_configuration import LoggingConfiguration
from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.model.processes.calls_process import CallsProcess
from grortir.main.model.stages.cumulated_calls_stage import CumulatedCallsStage
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.calls_optimization_strategy import \
    CallsOptimizationStrategy
from grortir.main.pso.credit_calls_optimization_strategy import \
    CreditCallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm

LOG = logging.getLogger(__name__)


def create_input_vector_for_cumulated_stages(dimensions):
    length_of_input_vector = (dimensions + 1)
    return (0,) * length_of_input_vector


def create_stages(how_many_stages, max_calls, input_vector, expected_quality):
    return [CumulatedCallsStage(i, max_calls, input_vector, expected_quality)
            for i in
            range(how_many_stages)]


def create_edges_balanced(process, stages):
    for i in range(7):
        process.add_edge(stages[i], stages[2 * i + 1])
        process.add_edge(stages[i], stages[2 * i + 2])


def create_edges_unbalanced(process, stages):
    for i in range(3):
        process.add_edge(stages[i], stages[2 * i + 1])
        process.add_edge(stages[i], stages[2 * i + 2])
    process.add_edge(stages[5], stages[7])
    process.add_edge(stages[5], stages[8])
    process.add_edge(stages[6], stages[9])
    process.add_edge(stages[6], stages[10])
    process.add_edge(stages[9], stages[11])
    process.add_edge(stages[9], stages[12])
    process.add_edge(stages[10], stages[13])
    process.add_edge(stages[10], stages[14])


class PSO_algorithm_BFS_balanced_SEQ:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector, expected_quality,
               how_many_particles):
        bfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        bfs_process = CallsProcess()
        create_edges_balanced(bfs_process, bfs_stages)
        bfs_ordered_stages = bfs_stages
        bfs_grouping_strategy = GroupingStrategy(bfs_ordered_stages)
        for stage in bfs_ordered_stages:
            bfs_grouping_strategy.define_group([stage])
        bfs_optimization_strategy = CallsOptimizationStrategy()
        return PsoAlgorithm(bfs_process, bfs_grouping_strategy,
                            bfs_optimization_strategy, how_many_particles)


class PSO_algorithm_BFS_balanced_SIM:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector, expected_quality,
               how_many_particles):
        bfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        bfs_process = CallsProcess()
        create_edges_balanced(bfs_process, bfs_stages)
        bfs_ordered_stages = bfs_stages
        bfs_grouping_strategy = GroupingStrategy(bfs_ordered_stages)
        bfs_grouping_strategy.define_group(bfs_ordered_stages)
        bfs_optimization_strategy = CallsOptimizationStrategy()
        return PsoAlgorithm(bfs_process, bfs_grouping_strategy,
                            bfs_optimization_strategy, how_many_particles)


class PSO_algorithm_DFS_balanced_SEQ:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector, expected_quality,
               how_many_particles):
        dfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        dfs_process = CallsProcess()
        create_edges_balanced(dfs_process, dfs_stages)
        dfs_ordered_stages = get_dfs_balanced_ordered_stages(dfs_stages)
        dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
        for stage in dfs_ordered_stages:
            dfs_grouping_strategy.define_group([stage])
        dfs_optimization_strategy = CallsOptimizationStrategy()
        return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                            dfs_optimization_strategy, how_many_particles)


class PSO_algorithm_DFS_CREDIT_balanced_SEQ:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector,
               expected_quality,
               how_many_particles):
        dfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        dfs_process = CallsProcess()
        create_edges_balanced(dfs_process, dfs_stages)
        dfs_ordered_stages = get_dfs_balanced_ordered_stages(dfs_stages)
        dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
        for stage in dfs_ordered_stages:
            dfs_grouping_strategy.define_group([stage])
        dfs_optimization_strategy = CreditCallsOptimizationStrategy()
        return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                            dfs_optimization_strategy, how_many_particles)


class PSO_algorithm_DFS_unbalanced_SEQ:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector, expected_quality,
               how_many_particles):
        dfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        dfs_process = CallsProcess()
        create_edges_unbalanced(dfs_process, dfs_stages)
        dfs_ordered_stages = get_dfs_unbalanced_ordered_stages(dfs_stages)
        dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
        for stage in dfs_ordered_stages:
            dfs_grouping_strategy.define_group([stage])
        dfs_optimization_strategy = CallsOptimizationStrategy()
        return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                            dfs_optimization_strategy, how_many_particles)


class PSO_algorithm_DFS_CREDIT_unbalanced_SEQ:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector,
               expected_quality,
               how_many_particles):
        dfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        dfs_process = CallsProcess()
        create_edges_unbalanced(dfs_process, dfs_stages)
        dfs_ordered_stages = get_dfs_unbalanced_ordered_stages(dfs_stages)
        dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
        for stage in dfs_ordered_stages:
            dfs_grouping_strategy.define_group([stage])
        dfs_optimization_strategy = CreditCallsOptimizationStrategy()
        return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                            dfs_optimization_strategy, how_many_particles)


class PSO_algorithm_DFS_balanced_SIM:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector, expected_quality,
               how_many_particles):
        dfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        dfs_process = CallsProcess()
        create_edges_balanced(dfs_process, dfs_stages)
        dfs_ordered_stages_balanced = get_dfs_balanced_ordered_stages(
            dfs_stages)
        dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages_balanced)
        dfs_grouping_strategy.define_group(dfs_ordered_stages_balanced)
        dfs_optimization_strategy = CallsOptimizationStrategy()
        return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                            dfs_optimization_strategy, how_many_particles)


class PSO_algorithm_DFS_unbalanced_SIM:
    @staticmethod
    def create(how_many_stages, max_calls,
               input_vector, expected_quality,
               how_many_particles):
        dfs_stages = create_stages(how_many_stages, max_calls, input_vector,
                                   expected_quality)
        dfs_process = CallsProcess()
        create_edges_unbalanced(dfs_process, dfs_stages)
        dfs_ordered_stages_unbalanced = get_dfs_unbalanced_ordered_stages(
            dfs_stages)
        dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages_unbalanced)
        dfs_grouping_strategy.define_group(dfs_ordered_stages_unbalanced)
        dfs_optimization_strategy = CallsOptimizationStrategy()
        return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                            dfs_optimization_strategy, how_many_particles)


def get_dfs_balanced_ordered_stages(stages):
    return [
        stages[0],
        stages[1],
        stages[3],
        stages[7],
        stages[8],
        stages[4],
        stages[9],
        stages[10],
        stages[2],
        stages[5],
        stages[11],
        stages[12],
        stages[6],
        stages[13],
        stages[14]
    ]


def get_dfs_unbalanced_ordered_stages(stages):
    return [
        stages[0],
        stages[1],
        stages[3],
        stages[4],
        stages[2],
        stages[5],
        stages[7],
        stages[8],
        stages[6],
        stages[9],
        stages[11],
        stages[12],
        stages[10],
        stages[13],
        stages[14]
    ]


def run_all(dimensions, max_calls, expected_quality, how_many_tries,
            how_many_particles, algorithmsToRun):
    how_many_stages = 15

    success_count = {}
    for algorithm in algorithmsToRun:
        success_count[algorithm.__name__] = 0

    for algorithm in algorithmsToRun:
        for i in range(how_many_tries):
            input_vector = create_input_vector_for_cumulated_stages(dimensions)
            pso = algorithm.create(
                how_many_stages, max_calls, input_vector, expected_quality,
                how_many_particles)
            LOG.info("Started " + algorithm.__name__)
            pso.run()
            if pso.process.optimization_status == OptimizationStatus.success:
                success_count[algorithm.__name__] += 1
                LOG.info(algorithm.__name__ + " SUCCESS!")

            LOG.info("Iteracja:" + str(i))

    LOG.info("***SUMMARY INFO: ***")
    LOG.info(
        "Max calls, expected_quality, dim, how_many_particles, how_many_tries, X^2")
    LOG.info(
        str([max_calls, expected_quality, dimensions, how_many_particles,
             how_many_tries]))

    for algorithm in algorithmsToRun:
        LOG.info(
            algorithm.__name__ + ": " + str(success_count[algorithm.__name__]))


LoggingConfiguration.init()

MAX_CALLS = 1000
EXPECTED_QUALITY = 0.001
HOW_MANY_PARTICLES = 40
HOW_MANY_TRIES = 100
DIMENSIONS = [5]
ALGORITHMS_TO_RUN = [
    # PSO_algorithm_DFS_balanced_SEQ,
    # PSO_algorithm_DFS_CREDIT_balanced_SEQ,
    PSO_algorithm_DFS_unbalanced_SEQ,
    PSO_algorithm_DFS_CREDIT_unbalanced_SEQ
]

for dimensions in DIMENSIONS:
    run_all(dimensions, MAX_CALLS, EXPECTED_QUALITY, HOW_MANY_TRIES,
            HOW_MANY_PARTICLES, ALGORITHMS_TO_RUN)
