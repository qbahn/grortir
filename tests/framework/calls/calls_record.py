# pylint: disable=too-many-arguments


class CallRecord:
    def __init__(self, entity_name, method_name, input_parms_list, output,
                 count):
        self.entity_name = entity_name
        self.count = count
        self.output = output
        self.input_parms_list = input_parms_list
        self.method_name = method_name
