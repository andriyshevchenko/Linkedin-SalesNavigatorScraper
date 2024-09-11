import better_exceptions

class ErrorLog:
    def __init__(self, error):
        self.error

    def __str__(self):
        return  better_exceptions.format_exception(self.error)