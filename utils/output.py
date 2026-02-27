"""
Output formatter for displaying scheduling results.
"""

from typing import List, Dict
from .process import Process


class OutputFormatter:
    """Handles formatting and displaying of scheduling results."""
    
    def __init__(self, last_instant: int, processes: List[Process]):
        self.last_instant = last_instant
        self.processes = processes
        self.timeline = {}  # {process_name: [state_at_time_0, state_at_time_1, ...]}
        self._init_timeline()
    
    def _init_timeline(self):
        """Initialize empty timeline for all processes."""
        for process in self.processes:
            self.timeline[process.name] = [' '] * self.last_instant
    
    def reset(self):
        """Reset timeline."""
        self._init_timeline()
    
    def mark_executing(self, process_name: str, time: int):
        """Mark a process as executing at a given time."""
        if 0 <= time < self.last_instant:
            self.timeline[process_name][time] = '*'
    
    def mark_waiting(self, process_name: str, time: int):
        """Mark a process as waiting at a given time."""
        if 0 <= time < self.last_instant:
            # Only mark as waiting if not already marked as executing
            if self.timeline[process_name][time] == ' ':
                self.timeline[process_name][time] = '.'
    
    def print_trace(self, algorithm_name: str):
        """Print timeline in trace format."""
        # Print header with time units
        print(f"{algorithm_name:6}", end="")
        for i in range(self.last_instant):
            print(f"{i % 10:2}", end="")
        print(" ")
        
        # Print separator
        print("-" * (6 + self.last_instant * 2 + 1))
        
        # Print each process timeline
        for process in self.processes:
            print(f"{process.name:6}|", end="")
            for state in self.timeline[process.name]:
                print(f"{state}|", end="")
            print(" ")
        
        # Print separator
        print("-" * (6 + self.last_instant * 2 + 1))
    
    def print_stats(self, algorithm_name: str):
        """Print statistics table."""
        print(f"{algorithm_name:12}", end="")
        for process in self.processes:
            print(f"{process.name:5}", end="")
        print()
        
        # Arrival times
        print(f"{'Arrival':12}", end="")
        for process in self.processes:
            print(f"{process.arrival_time:5}", end="")
        print()
        
        # Service times
        print(f"{'Service':12}", end="")
        for process in self.processes:
            print(f"{process.service_time:5}", end="")
        print()
        
        # Finish times
        print(f"{'Finish':12}", end="")
        for process in self.processes:
            print(f"{process.finish_time:5}", end="")
        print()
        
        # Turnaround times
        print(f"{'Turnaround':12}", end="")
        for process in self.processes:
            print(f"{process.turnaround_time:5}", end="")
        print()
        
        # Normalized turnaround
        print(f"{'NormTurn':12}", end="")
        for process in self.processes:
            print(f"{process.normalized_turnaround:5.2f}", end="")
        print()
