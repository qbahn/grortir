"""Validate process."""


class ProcessValidator(object):
    """Validate if process is correctly defined."""
    @staticmethod
    def validate(process):
        """Main method."""
        return process is not None
