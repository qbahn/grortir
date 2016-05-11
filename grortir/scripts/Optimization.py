# pylint: skip-file
from grortir.main.model.processes.factories.calls_process_factory import \
    CallsProcessFactory
from grortir.main.optimizers.optimizer import Optimizer

five_stage_process = CallsProcessFactory("linear", 5, 1000,
                                         (0, 0, 0)).construct_process()
optimizer = Optimizer(five_stage_process)
optimizer.optimize_process()
print("end!")
