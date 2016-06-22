"""Class represents grouping strategy."""


class GroupingStrategy(object):
    """Class represents grouping strategy."""

    def __init__(self, ordered_stages):
        self.ordered_stages = ordered_stages
        self.groups = {}
        pass

    def define_group(self, group_of_stages):
        """Add group of stages. Those stages will be in the same group.

        Args:
            group_of_stages (tuple): group of stages"""
        group_number = self.get_actual_numbers_of_groups()
        for stage in group_of_stages:
            if stage in self.groups.keys():
                raise ValueError("Stage already added.")
            else:
                self.ordered_stages[stage] = group_number

    def get_actual_numbers_of_groups(self):
        if len(self.groups) == 0:
            return 0
        else:
            return sorted(self.groups.values())[-1] + 1

    def get_items_from_the_same_group(self, stage):
        group_number = self.groups[stage]
        stages_from_group = []
        for cur_stage in self.groups.keys():
            if self.groups[cur_stage] == group_number:
                stages_from_group.append(cur_stage)
