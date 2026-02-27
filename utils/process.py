"""
Process class to represent a single process in the scheduling simulation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Process:
    """Represents a single process with all its attributes."""
    
    name: str
    arrival_time: int
    service_time: int
    priority: int = 0  # Used for Aging algorithm
    
    # Calculated during scheduling
    finish_time: int = 0
    turnaround_time: int = 0
    normalized_turnaround: float = 0.0
    
    # Runtime state
    remaining_time: int = 0
    start_time: Optional[int] = None
    wait_time: int = 0
    
    def __post_init__(self):
        """Initialize remaining time after creation."""
        self.remaining_time = self.service_time
    
    def reset(self):
        """Reset process state for a new scheduling run."""
        self.remaining_time = self.service_time
        self.finish_time = 0
        self.turnaround_time = 0
        self.normalized_turnaround = 0.0
        self.start_time = None
        self.wait_time = 0
    
    def calculate_stats(self):
        """Calculate turnaround time and normalized turnaround."""
        self.turnaround_time = self.finish_time - self.arrival_time
        if self.service_time > 0:
            self.normalized_turnaround = self.turnaround_time / self.service_time
        else:
            self.normalized_turnaround = 0.0
    
    def __repr__(self):
        return (f"Process({self.name}, arrival={self.arrival_time}, "
                f"service={self.service_time}, remaining={self.remaining_time})")
    
    def __lt__(self, other):
        """For sorting/priority queue comparisons."""
        return self.arrival_time < other.arrival_time
