"""Module which represent process which can be optimized."""

import networkx as nx


class AbstractProcess(nx.DiGraph):
    """Class which represent process which can be optimized."""

    def __init__(self):
        """Constructor."""
        nx.DiGraph.__init__(self)
