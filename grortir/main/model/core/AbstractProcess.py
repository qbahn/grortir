"""Module which represent process which can be optimized."""

import networkx as nx


class AbstractProcess(nx.DiGraph):
    """Class which represent process which can be optimized."""

    def __init__(self):
        """
        Constructor.

        :param self: AbstractProcess
        """
        nx.DiGraph.__init__(self)
