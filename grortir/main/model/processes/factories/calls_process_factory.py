"""Contains factory class of process with calls stages."""

from grortir.main.model.processes.calls_process import CallsProcess
from grortir.main.model.stages.calls_stage import CallsStage


class CallsProcessFactory:
    """Class which produce process with the same type of stages.

    Attributes:
        structure_type (str): represent type of structure
        how_many_nodes (int): how many nodes should be in generated process
        max_calls (int): max_calls for stages
        process (CallsProcess): process which will be incrementally build
        initial_vec (tuple): initial vector
    """

    def __init__(self, structure_type, how_many_nodes, max_calls,
                 initial_vec=()):
        """Constructor."""
        self.max_calls = max_calls
        self._stages_to_add = []
        self.structure_type = structure_type
        self.how_many_nodes = how_many_nodes
        self.process = CallsProcess()
        self.initial_vec = initial_vec

    def _update_structure(self):
        """Update structure of process."""
        if self.structure_type == "linear":
            if len(self._stages_to_add) > 1:
                self.process.add_path(self._stages_to_add)
            else:
                self.process.add_node(self._stages_to_add[0])
        else:
            raise NotImplementedError()

    def _create_stages(self):
        """Create stages which will be injected to process."""
        for i in range(self.how_many_nodes):
            self._stages_to_add += [
                CallsStage(str(i), self.max_calls, self.initial_vec)]

    def construct_process(self):
        """Construct process."""
        self._create_stages()
        self._update_structure()
        return self.process
