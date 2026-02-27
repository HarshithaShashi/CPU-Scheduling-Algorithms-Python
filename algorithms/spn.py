"""
Shortest Process Next (SPN) scheduling algorithm.
"""

from .base import SchedulerBase


class SPN(SchedulerBase):
    """
    Shortest Process Next scheduling algorithm.
    Non-preemptive: Always selects the process with shortest service time.
    """
    
    def schedule(self):
        """Implement SPN scheduling."""
        current_time = 0
        completed = []
        
        while len(completed) < len(self.processes):
            # Get all arrived processes that haven't completed
            available = [p for p in self.processes 
                        if p.arrival_time <= current_time 
                        and p not in completed]
            
            if not available:
                # No process available, advance to next arrival
                next_arrival = min(p.arrival_time for p in self.processes if p not in completed)
                current_time = next_arrival
                continue
            
            # Select process with shortest service time
            process = min(available, key=lambda p: p.service_time)
            
            # Execute the process to completion
            for t in range(current_time, current_time + process.service_time):
                if t < self.last_instant:
                    self.output.mark_executing(process.name, t)
                    self._mark_waiting_processes(t, process)
            
            current_time += process.service_time
            process.finish_time = current_time
            process.remaining_time = 0
            completed.append(process)
