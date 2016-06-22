import networkx as nx

from grortir.main.model.processes.calls_process import CallsProcess
from grortir.main.model.processes.factories.calls_process_factory import CallsProcessFactory
from grortir.main.model.stages.calls_stage import CallsStage
from grortir.main.optimizers.grouped_optimizer import GroupedOptimizer
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm

#
# calls_factory = CallsProcessFactory("linear", 1, 1000, [0, 0, 0])
# process = calls_factory.construct_process()
#
# ordered_stages = nx.topological_sort(process)
#
process = CallsProcess()
stage = CallsStage("stage_name", 1000, [0])
process.add_node(stage)
ordered_stages = [stage]

grouping_strategy = GroupingStrategy(ordered_stages)
grouping_strategy.define_group(ordered_stages)

pso_algortihm = PsoAlgorithm(process, grouping_strategy, 1)
optimizer = GroupedOptimizer(process, grouping_strategy, pso_algortihm)

optimizer.optimize_process()

optimizer.result
