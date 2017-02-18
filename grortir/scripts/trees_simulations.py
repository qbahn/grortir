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
EXPECTED_QUALITY = 3.8
INPUT_VECTOR = (0,)
HOW_MANY_PARTICLES = 40
HOW_MANY_TRIES = 100


def create_stages():
    return [CumulatedCallsStage(i, MAX_CALLS, INPUT_VECTOR, EXPECTED_QUALITY) for i in
            range(15)]


def create_edges(process, stages):
    for i in range(7):
        process.add_edge(stages[i], stages[2 * i + 1])
        process.add_edge(stages[i], stages[2 * i + 2])


def create_PSO_algorithm_BFS_SEQ():
    bfs_stages = create_stages()
    bfs_process = CallsProcess()
    create_edges(bfs_process, bfs_stages)
    bfs_ordered_stages = bfs_stages
    bfs_grouping_strategy = GroupingStrategy(bfs_ordered_stages)
    for stage in bfs_ordered_stages:
        bfs_grouping_strategy.define_group([stage])
    bfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(bfs_process, bfs_grouping_strategy,
                        bfs_optimization_strategy, HOW_MANY_PARTICLES)


def create_PSO_algorithm_BFS_SIM():
    bfs_stages = create_stages()
    bfs_process = CallsProcess()
    create_edges(bfs_process, bfs_stages)
    bfs_ordered_stages = bfs_stages
    bfs_grouping_strategy = GroupingStrategy(bfs_ordered_stages)
    bfs_grouping_strategy.define_group(bfs_ordered_stages)
    bfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(bfs_process, bfs_grouping_strategy,
                        bfs_optimization_strategy, HOW_MANY_PARTICLES)


# BFS part


def create_PSO_algorithm_DFS_SEQ():
    dfs_stages = create_stages()
    dfs_process = CallsProcess()
    create_edges(dfs_process, dfs_stages)
    dfs_ordered_stages = [
        dfs_stages[0],
        dfs_stages[1],
        dfs_stages[3],
        dfs_stages[7],
        dfs_stages[8],
        dfs_stages[4],
        dfs_stages[9],
        dfs_stages[10],
        dfs_stages[2],
        dfs_stages[5],
        dfs_stages[11],
        dfs_stages[12],
        dfs_stages[6],
        dfs_stages[13],
        dfs_stages[14]
    ]
    dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
    for stage in dfs_ordered_stages:
        dfs_grouping_strategy.define_group([stage])
    dfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                        dfs_optimization_strategy, HOW_MANY_PARTICLES)


def create_PSO_algorithm_DFS_SIM():
    dfs_stages = create_stages()
    dfs_process = CallsProcess()
    create_edges(dfs_process, dfs_stages)
    dfs_ordered_stages = [
        dfs_stages[0],
        dfs_stages[1],
        dfs_stages[3],
        dfs_stages[7],
        dfs_stages[8],
        dfs_stages[4],
        dfs_stages[9],
        dfs_stages[10],
        dfs_stages[2],
        dfs_stages[5],
        dfs_stages[11],
        dfs_stages[12],
        dfs_stages[6],
        dfs_stages[13],
        dfs_stages[14]
    ]
    dfs_grouping_strategy = GroupingStrategy(dfs_ordered_stages)
    dfs_grouping_strategy.define_group(dfs_ordered_stages)
    dfs_optimization_strategy = CallsOptimizationStrategy()
    return PsoAlgorithm(dfs_process, dfs_grouping_strategy,
                        dfs_optimization_strategy, HOW_MANY_PARTICLES)


# DFS part
dfs_results = []
dfs_success_count_SIM = 0
bfs_success_count_SIM = 0
dfs_success_count_SEQ = 0
bfs_success_count_SEQ = 0
for i in range(HOW_MANY_TRIES):
    dfs_pso_SIM = create_PSO_algorithm_DFS_SIM()
    dfs_pso_SIM.run()
    if dfs_pso_SIM.process.optimization_status == OptimizationStatus.success:
        dfs_success_count_SIM += 1
        print("DFS SIM SUCCESS!")
    bfs_pso_SIM = create_PSO_algorithm_BFS_SIM()
    bfs_pso_SIM.run()
    if bfs_pso_SIM.process.optimization_status == OptimizationStatus.success:
        bfs_success_count_SIM += 1
        print("BFS SIM SUCCESS!")

    dfs_pso_SEQ = create_PSO_algorithm_DFS_SEQ()
    dfs_pso_SEQ.run()
    if dfs_pso_SEQ.process.optimization_status == OptimizationStatus.success:
        dfs_success_count_SEQ += 1
        print("DFS SEQ SUCCESS!")
    bfs_pso_SEQ = create_PSO_algorithm_BFS_SEQ()
    bfs_pso_SEQ.run()
    if bfs_pso_SEQ.process.optimization_status == OptimizationStatus.success:
        bfs_success_count_SEQ += 1
        print("BFS SEQ SUCCESS!")
    print("Iteracja:" + str(i))

print("Max calls, expected_quality, dim, how_many_particles, how_many_tries, NEW_FUNCTION")
print(str([MAX_CALLS, EXPECTED_QUALITY, len(INPUT_VECTOR), HOW_MANY_PARTICLES,
           HOW_MANY_TRIES]))
#
print("DFS SIM count:" + str(dfs_success_count_SIM))
print("BFS SIM count:" + str(bfs_success_count_SIM))
print("DFS SEQ count:" + str(dfs_success_count_SEQ))
print("BFS SEQ count:" + str(bfs_success_count_SEQ))
