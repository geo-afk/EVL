class ScopeException(Exception):
    pass

class EVALTypeException(Exception):
    pass

class EVALNameException(EVALTypeException):
    pass

class EVALConstException(Exception):
    pass