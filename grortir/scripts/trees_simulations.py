import matplotlib.pyplot as plt

from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.model.processes.calls_process import CallsProcess
from grortir.main.model.stages.cumulated_calls_stage import CumulatedCallsStage
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.calls_optimization_strategy import \
    CallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm


def draw_from_dict(dict_with_results, name="Undefined"):
    x = []
    y = []
    for key, value in dict_with_results.items():
        x.append(key)
        y.append(value)
    plt.plot(x, y, 'ro')
    plt.savefig(name)
    plt.show()


def calculate_probability_of_success(max_calls, number_of_nodes,
                                     number_of_tries, method_type):
    results = {}
    for how_many_nodes in number_of_nodes:
        how_many_success = 0.0
        how_many_failed = 0.0
        probability = -1
        for nr_proby in range(number_of_tries):
            optimized_process = optimization(max_calls, how_many_nodes,
                                             method_type)
            if optimized_process.optimization_status == OptimizationStatus.success:
                how_many_success += 1
            else:
                how_many_failed += 1
            probability = how_many_success / number_of_tries
        results[how_many_nodes] = probability
    return results


MAX_CALLS = 1000
EXPECTED_QUALITY = 0.1
INPUT_VECTOR = (0,)
HOW_MANY_PARTICLES = 40
HOW_MANY_TRIES = 100


def create_stages():
    return [CumulatedCallsStage(i, MAX_CALLS, INPUT_VECTOR, EXPECTED_QUALITY)
            for i in
            range(15)]


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


def create_PSO_algorithm_BFS_balanced_SEQ():
    bfs_stages = create_stages()
    bfs_process = CallsProcess()
    create_edges_balanced(bfs_process, bfs_stages)
    bfs_ordered_stages = bfs_stages
    bfs_grouping_strategy = GroupingStrategy(bfs_ordered_stages)
    for stage in bfs_ordered_stages:
        bfs_grouping_strategy.define_group([stage])
    bfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(bfs_process, bfs_grouping_strategy,
                        bfs_optimization_strategy, HOW_MANY_PARTICLES)


def create_PSO_algorithm_BFS_balanced_SIM():
    bfs_stages = create_stages()
    bfs_process = CallsProcess()
    create_edges_balanced(bfs_process, bfs_stages)
    bfs_ordered_stages = bfs_stages
    bfs_grouping_strategy = GroupingStrategy(bfs_ordered_stages)
    bfs_grouping_strategy.define_group(bfs_ordered_stages)
    bfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(bfs_process, bfs_grouping_strategy,
                        bfs_optimization_strategy, HOW_MANY_PARTICLES)


# BFS part


def create_PSO_algorithm_DFS_balanced_SEQ():
    dfs_stages = create_stages()
    dfs_process = CallsProcess()
    create_edges_balanced(dfs_process, dfs_stages)
    dfs_ordered_stages = get_dfs_balanced_ordered_stages(dfs_stages)
    dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
    for stage in dfs_ordered_stages:
        dfs_grouping_strategy.define_group([stage])
    dfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                        dfs_optimization_strategy, HOW_MANY_PARTICLES)


def create_PSO_algorithm_DFS_unbalanced_SEQ():
    dfs_stages = create_stages()
    dfs_process = CallsProcess()
    create_edges_unbalanced(dfs_process, dfs_stages)
    dfs_ordered_stages = get_dfs_unbalanced_ordered_stages(dfs_stages)
    dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
    for stage in dfs_ordered_stages:
        dfs_grouping_strategy.define_group([stage])
    dfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                        dfs_optimization_strategy, HOW_MANY_PARTICLES)


def create_PSO_algorithm_DFS_balanced_SIM():
    dfs_stages = create_stages()
    dfs_process = CallsProcess()
    create_edges_balanced(dfs_process, dfs_stages)
    dfs_ordered_stages_balanced = get_dfs_balanced_ordered_stages(dfs_stages)
    dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages_balanced)
    dfs_grouping_strategy.define_group(dfs_ordered_stages_balanced)
    dfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                        dfs_optimization_strategy, HOW_MANY_PARTICLES)


def create_PSO_algorithm_DFS_unbalanced_SIM():
    dfs_stages = create_stages()
    dfs_process = CallsProcess()
    create_edges_unbalanced(dfs_process, dfs_stages)
    dfs_ordered_stages_unbalanced = get_dfs_unbalanced_ordered_stages(
        dfs_stages)
    dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages_unbalanced)
    dfs_grouping_strategy.define_group(dfs_ordered_stages_unbalanced)
    dfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                        dfs_optimization_strategy, HOW_MANY_PARTICLES)


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


# DFS part
dfs_results = []
dfs_success_balanced_count_SIM = 0
dfs_unbalanced_success_count_SIM = 0
dfs_balanced_success_count_SEQ = 0
dfs_unbalanced_success_count_SEQ = 0
for i in range(HOW_MANY_TRIES):
    dfs_pso_balanced_SIM = create_PSO_algorithm_DFS_balanced_SIM()
    dfs_pso_balanced_SIM.run()
    if dfs_pso_balanced_SIM.process.optimization_status == OptimizationStatus.success:
        dfs_success_balanced_count_SIM += 1
        print("DFS balanced SIM SUCCESS!")
    dfs_pso_unbalanced_SIM = create_PSO_algorithm_DFS_unbalanced_SIM()
    dfs_pso_unbalanced_SIM.run()
    if dfs_pso_unbalanced_SIM.process.optimization_status == OptimizationStatus.success:
        dfs_unbalanced_success_count_SIM += 1
        print("DFS unbalanced SIM SUCCESS!")

    dfs_pso_balanced_SEQ = create_PSO_algorithm_DFS_balanced_SEQ()
    dfs_pso_balanced_SEQ.run()
    if dfs_pso_balanced_SEQ.process.optimization_status == OptimizationStatus.success:
        dfs_balanced_success_count_SEQ += 1
        print("DFS balanced SEQ SUCCESS!")
    dfs_pso_unbalanced_SEQ = create_PSO_algorithm_DFS_unbalanced_SEQ()
    dfs_pso_unbalanced_SEQ.run()
    if dfs_pso_unbalanced_SEQ.process.optimization_status == OptimizationStatus.success:
        dfs_unbalanced_success_count_SEQ += 1
        print("DFS unbalanced SEQ SUCCESS!")
    print("Iteracja:" + str(i))

print(
    "Max calls, expected_quality, dim, how_many_particles, how_many_tries, NEW_FUNCTION")
print(str([MAX_CALLS, EXPECTED_QUALITY, len(INPUT_VECTOR), HOW_MANY_PARTICLES,
           HOW_MANY_TRIES]))
#
print("dfs_success_balanced_count_SIM: " + str(dfs_success_balanced_count_SIM))
print(
    "dfs_unbalanced_success_count_SIM: " + str(dfs_unbalanced_success_count_SIM))
print("dfs_balanced_success_count_SEQ: " + str(dfs_balanced_success_count_SEQ))
print(
    "dfs_unbalanced_success_count_SEQ: " + str(dfs_unbalanced_success_count_SEQ))
