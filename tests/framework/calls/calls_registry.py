from tests.framework.calls.calls_record import CallRecord


# pylint: disable=too-many-arguments


class CallsRegistry:
    def __init__(self):
        self.calls_storage = {}
        self.calls_counter = 0

    def register_call(self, call_record):
        """
        Register call.
        Args:
            call_record (CallRecord): represent call
        """
        self.calls_counter += 1
        if self.calls_storage.get(call_record.entity_name) is None:
            self.calls_storage[call_record.entity_name] = {}
        if self.calls_storage[call_record.entity_name].get(
                call_record.method_name) is None:
            self.calls_storage[call_record.entity_name][
                call_record.method_name] = []
        self.calls_storage[call_record.entity_name][
            call_record.method_name].append({"call": call_record,
                                             "calls_count": self.calls_counter})

    def get_method_calls(self, entity_name, method_name):
        """
        Return calls
        Args:
            entity_name (str): name of entity
            method_name (str): name of method called on entity

        Returns:
            list: list of call objects  (CallRecord)

        """
        return self.calls_storage[entity_name][method_name]

    def add_call(self, entity_name, method_name, input_parms_list, output,
                 count):
        """Add and register call of function.

        Args:
            entity_name (str): name of entity
            method_name (str): name of method
            input_parms_list (list): list of arguments put to function
            output (object):  returned value by method_name
            count (int): number of count
        """
        call_record = CallRecord(entity_name, method_name, input_parms_list,
                                 output, count)
        self.register_call(call_record)
