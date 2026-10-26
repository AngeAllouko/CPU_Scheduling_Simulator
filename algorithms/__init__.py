"""
CPU Scheduling Algorithms package.
"""

from .fcfs import fcfs
from .sjf import sjf
from .srtf import srtf
from .priority import priority
from .round_robin import round_robin

__all__ = ["fcfs", "sjf", "srtf", "priority", "round_robin"]
