import networkx as nx

from grortir.main.model.processes.factories.calls_process_factory import \
    CallsProcessFactory
from grortir.main.optimizers.grouped_optimizer import GroupedOptimizer
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.calls_optimization_strategy import \
    CallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm

how_many_particles = 2
calls_factory = CallsProcessFactory("linear", 10, how_many_particles*1000, [0, 0, 0, 0])
process = calls_factory.construct_process()

ordered_stages = nx.topological_sort(process)

# process = CallsProcess()
# stage = CallsStage("stage_name", 1000, [0])
# process.add_node(stage)
# ordered_stages = [stage]

grouping_strategy = GroupingStrategy(ordered_stages)
grouping_strategy.define_group(ordered_stages)
optimization_startegy = CallsOptimizationStrategy()

pso_algortihm = PsoAlgorithm(process, grouping_strategy, optimization_startegy,
                             how_many_particles)
optimizer = GroupedOptimizer(process, grouping_strategy, pso_algortihm)

optimizer.optimize_process()

optimizer.result
