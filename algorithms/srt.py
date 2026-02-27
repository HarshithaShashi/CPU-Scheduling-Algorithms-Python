"""
Shortest Remaining Time (SRT) scheduling algorithm.
"""

from .base import SchedulerBase


class SRT(SchedulerBase):
    """
    Shortest Remaining Time scheduling algorithm.
    Preemptive: Can switch to a new process with shorter remaining time.
    """
    
    def schedule(self):
        """Implement SRT scheduling."""
        current_time = 0
        completed = 0
        total_processes = len(self.processes)
        
        while completed < total_processes and current_time < self.last_instant:
            # Get all arrived processes with remaining time
            available = [p for p in self.processes 
                        if p.arrival_time <= current_time 
                        and p.remaining_time > 0]
            
            if not available:
                # No process available, advance to next arrival
                next_arrivals = [p.arrival_time for p in self.processes if p.remaining_time > 0]
                if next_arrivals:
                    current_time = min(next_arrivals)
                else:
                    break
                continue
            
            # Select process with shortest remaining time
            process = min(available, key=lambda p: p.remaining_time)
            
            # Execute for 1 time unit
            self.output.mark_executing(process.name, current_time)
            self._mark_waiting_processes(current_time, process)
            
            process.remaining_time -= 1
            current_time += 1
            
            # Check if process completed
            if process.remaining_time == 0:
                process.finish_time = current_time
                completed += 1
