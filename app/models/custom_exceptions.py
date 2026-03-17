class ScopeException(Exception):
    pass

class EVALTypeException(Exception):
    pass

class EVALNameException(EVALTypeException):
    pass

class EVALConstException(Exception):
    pass


class CastException(Exception):
    pass

class DeclarationException(Exception):
    pass


class CoercionException(Exception):
    pass

class PowException(Exception):
    pass
