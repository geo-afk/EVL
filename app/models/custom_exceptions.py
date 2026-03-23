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



class BreakSignal(Exception):
    """Raised by visitBreakStatement to unwind to the nearest enclosing loop."""

class ContinueSignal(Exception):
    """Raised by visitContinueStatement to skip to the next loop iteration."""
