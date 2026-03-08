# src/pycea/__init__.py
__version__ = "0.1.0"

from .core import CEA, Species, Results

# Control what "from pycea import *" exposes
__all__ = [
    "CEA",
    "Species", 
    "Results",
]

