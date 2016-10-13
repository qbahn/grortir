"""Example when Sim is better than  sequential."""
import matplotlib.pyplot as plt
import networkx as nx

from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.model.processes.factories.calls_process_factory import \
    CallsProcessFactory
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.calls_optimization_strategy import \
    CallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm


def optimization(max_calls, how_many_nodes, method_type):
    factory = CallsProcessFactory("linear", how_many_nodes, max_calls, (0.216,))
    process = factory.construct_process()
    ordered_stages = nx.topological_sort(process)
    grouping_strategy = GroupingStrategy(ordered_stages)
    # in sim all stages are in the sam group:
    if method_type == "SIM":
        grouping_strategy.define_group(ordered_stages)
    elif method_type == "SEQ":
        for stage in ordered_stages:
            grouping_strategy.define_group([stage])
    else:
        raise NotImplementedError
    calls_optimization_strategy = CallsOptimizationStrategy()
    pso_algorithm = PsoAlgorithm(process, grouping_strategy,
                                 calls_optimization_strategy)
    pso_algorithm.run()
    return process


# sim_optimization(MAX_CALLS, HOW_MANY_NODES)
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


NUMBER_OF_STAGES = [1, 2, 3, 5, 7, 10]
HOW_MANY_TRIES = 100
MAX_CALLS = 1000


def draw_from_dict(dict_with_results, name="Undefined"):
    x = []
    y = []
    for key, value in dict_with_results.items():
        x.append(key)
        y.append(value)
    plt.plot(x, y, 'ro')
    plt.savefig(name)
    plt.show()


# key -dimension, value - probability of success
results_sim = calculate_probability_of_success(MAX_CALLS, NUMBER_OF_STAGES,
                                               HOW_MANY_TRIES,
                                               "SIM")
draw_from_dict(results_sim, "SIM_diagram.png")
# {1: 1.0, 2: 0.95, 3: 0.78, 5: 0.46, 7: 0.06, 10: 0.0}


results_seq = calculate_probability_of_success(MAX_CALLS, NUMBER_OF_STAGES,
                                               HOW_MANY_TRIES,
                                               "SEQ")
draw_from_dict(results_seq, "SEQ_diagram.png")
# {1: 1.0, 2: 0.0, 3: 0.0, 5: 0.0, 7: 0.0, 10: 0.0}

print("The End")
