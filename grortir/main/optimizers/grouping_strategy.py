"""Class represents grouping strategy."""
STAGE_NOT_IN_STRATEGY_ = "Stage not considered in strategy."


class GroupingStrategy(object):
    """Class represents grouping strategy.
    Attributes:
        ordred_stages (list): List of stages which represent order in strategy.
        groups (dict): Contains informations about groups.
                        Key is stage and value is number of group.
    """

    def __init__(self, ordered_stages):
        """Constructor."""
        self.ordered_stages = ordered_stages
        self.groups = {}

    def define_group(self, group_of_stages):
        """Add group of stages. Those stages will be in the same group.

        Raises:
            ValueError: If stage couldn't be added to new group.

        Args:
            group_of_stages (tuple): group of stages"""
        group_number = self.get_actual_numbers_of_groups()
        for stage in group_of_stages:
            if stage in self.groups.keys():
                raise ValueError("Stage already added.")
            elif stage not in self.ordered_stages:
                raise ValueError("Stage not considered in strategy.")
            else:
                self.groups[stage] = group_number

    def get_actual_numbers_of_groups(self):
        """Returns how many groups already.

        Returns:
            amount (int) : amount of groups
            """
        if len(self.groups) == 0:
            return 0
        else:
            return sorted(self.groups.values())[-1] + 1

    def get_items_from_the_same_group(self, stage):
        """Returns list of stages from group in which is already stage.
        Returns:
            list_of_stages (list): list of stages from group

        Raises:
            ValueError: If stage is not in strategy.

        Args:
            stage (AbstractStage): stage"""
        if stage not in self.groups:
            raise ValueError(STAGE_NOT_IN_STRATEGY_)
        group_number = self.groups[stage]
        stages_from_group = []
        for cur_stage in self.groups:
            if self.groups[cur_stage] == group_number:
                stages_from_group.append(cur_stage)
        return stages_from_group
