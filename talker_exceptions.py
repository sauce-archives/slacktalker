class TalkerException(Exception):
    pass


class UserNotFoundException(TalkerException):
    pass


class UserHasntSpoken(TalkerException):
    pass
