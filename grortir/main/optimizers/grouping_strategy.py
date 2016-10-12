"""Class represents grouping strategy."""
STAGE_NOT_IN_STRATEGY_ = "Stage not considered in strategy."


class GroupingStrategy(object):
    """Class represents grouping strategy.
    Attributes:
        ordred_stages (list): List of stages which represent order in strategy.
        groups (dict): Contains information about groups.
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
            int: amount of groups
            """
        if len(self.groups) == 0:
            return 0
        else:
            return sorted(self.groups.values())[-1] + 1

    def get_items_from_the_same_group(self, stage):
        """Returns list of stages from group in which is already stage.
        Returns:
            list: list of stages from group ordered as in self.ordered_stages

        Raises:
            ValueError: If stage is not in strategy.

        Args:
            stage (AbstractStage): stage"""
        if stage not in self.groups:
            raise ValueError(STAGE_NOT_IN_STRATEGY_)
        group_number = self.groups[stage]
        stages_from_group = []
        for cur_stage in self.ordered_stages:
            if self.groups[cur_stage] == group_number:
                stages_from_group.append(cur_stage)
        return stages_from_group

    def get_items_from_group(self, group_number):
        """Returns list of stages from group with 'group_number'.
            Returns:
                list: list of stages from group ordered as in
                 self.ordered_stages

            Raises:
                ValueError: If wrong number of groups.

            Args:
                group_number (int): number of group"""
        if group_number not in range(0, self.get_actual_numbers_of_groups()):
            raise ValueError
        stages_to_return = []
        for current_stage in self.ordered_stages:
            if self.groups[current_stage] == group_number:
                stages_to_return.append(current_stage)
        return stages_to_return
