"""
Aging scheduling algorithm.
"""

from .base import SchedulerBase


class Aging(SchedulerBase):
    """
    Aging scheduling algorithm.
    Uses priority-based scheduling with aging to prevent starvation.
    Every time the scheduler selects a process, it:
    1. Resets current process priority to initial priority
    2. Increments priority of all ready processes by 1
    3. Selects highest priority process
    """
    
    def __init__(self, processes, last_instant, output_formatter, quantum):
        super().__init__(processes, last_instant, output_formatter)
        self.quantum = quantum
        # Store initial priorities
        self.initial_priority = {p: p.priority for p in processes}
        # Current priorities (higher value = higher priority)
        self.current_priority = {p: p.priority for p in processes}
    
    def schedule(self):
        """Implement Aging scheduling."""
        current_time = 0
        completed = 0
        total_processes = len(self.processes)
        current_process = None
        quantum_used = 0
        
        while completed < total_processes and current_time < self.last_instant:
            # Get all arrived processes with remaining time
            ready_processes = [p for p in self.processes 
                             if p.arrival_time <= current_time 
                             and p.remaining_time > 0]
            
            if not ready_processes:
                # No process available, advance to next arrival
                next_arrivals = [p.arrival_time for p in self.processes if p.remaining_time > 0]
                if next_arrivals:
                    current_time = min(next_arrivals)
                else:
                    break
                continue
            
            # If current process quantum expired or completed, select new process
            if current_process is None or quantum_used >= self.quantum or current_process.remaining_time == 0:
                # Reset current process priority if it exists
                if current_process is not None and current_process.remaining_time > 0:
                    self.current_priority[current_process] = self.initial_priority[current_process]
                
                # Age all ready processes (except current)
                for p in ready_processes:
                    if p != current_process:
                        self.current_priority[p] += 1
                
                # Select process with highest priority
                current_process = max(ready_processes, 
                                    key=lambda p: (self.current_priority[p], -p.arrival_time))
                quantum_used = 0
            
            # Execute current process for 1 time unit
            self.output.mark_executing(current_process.name, current_time)
            self._mark_waiting_processes(current_time, current_process)
            
            current_process.remaining_time -= 1
            current_time += 1
            quantum_used += 1
            
            # Check if process completed
            if current_process.remaining_time == 0:
                current_process.finish_time = current_time
                completed += 1
                current_process = None
                quantum_used = 0
