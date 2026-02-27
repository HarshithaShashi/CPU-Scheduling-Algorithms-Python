"""
Base class for all scheduling algorithms.
"""

from abc import ABC, abstractmethod
from typing import List
from utils.process import Process
from utils.output import OutputFormatter


class SchedulerBase(ABC):
    """Abstract base class for all scheduling algorithms."""
    
    def __init__(self, processes: List[Process], last_instant: int, output_formatter: OutputFormatter):
        """
        Initialize scheduler.
        
        Args:
            processes: List of processes to schedule
            last_instant: Last time instant for simulation
            output_formatter: Output formatter for timeline/stats
        """
        self.processes = [p for p in processes]  # Create a copy
        self.last_instant = last_instant
        self.output = output_formatter
        self.current_time = 0
        
        # Reset all processes before scheduling
        for process in self.processes:
            process.reset()
    
    @abstractmethod
    def schedule(self):
        """
        Implement the scheduling algorithm.
        This method should be overridden by each specific algorithm.
        """
        pass
    
    def run(self):
        """Execute the scheduling algorithm and calculate statistics."""
        self.schedule()
        self._calculate_all_stats()
    
    def _calculate_all_stats(self):
        """Calculate statistics for all processes."""
        for process in self.processes:
            process.calculate_stats()
    
    def _get_arrived_processes(self, current_time: int) -> List[Process]:
        """Get all processes that have arrived by current_time."""
        return [p for p in self.processes if p.arrival_time <= current_time and p.remaining_time > 0]
    
    def _mark_waiting_processes(self, current_time: int, executing_process: Process = None):
        """Mark all arrived but not executing processes as waiting."""
        for process in self.processes:
            if (process.arrival_time <= current_time and 
                process.remaining_time > 0 and 
                process != executing_process):
                self.output.mark_waiting(process.name, current_time)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(processes={len(self.processes)})"
