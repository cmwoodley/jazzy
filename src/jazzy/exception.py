"""Anything about exceptions and their handling."""
# src/jazzy/exception.py


class JazzyError(Exception):
    """Raised when Jazzy cannot calculate results."""

    pass


class KallistoError(Exception):
    """Raised when something goes wrong inside kallisto."""

    pass


class NegativeLonePairsError(Exception):
    """Raised when a molecule contains negative lone pairs."""

    pass

class MMFFChargeCalculationError(Exception):
    """Raised when MMFF charge calculation fails."""

    pass


def exception_handling(func):
    """Catches core exceptions and raises a JazzyError."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (NegativeLonePairsError, KallistoError, MMFFChargeCalculationError) as e:
            raise JazzyError(str(e))

    return wrapper
