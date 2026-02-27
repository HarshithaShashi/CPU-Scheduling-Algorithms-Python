"""
Highest Response Ratio Next (HRRN) scheduling algorithm.
"""

from .base import SchedulerBase


class HRRN(SchedulerBase):
    """
    Highest Response Ratio Next scheduling algorithm.
    Non-preemptive: Selects process with highest response ratio.
    Response Ratio = (Waiting Time + Service Time) / Service Time
    """
    
    def schedule(self):
        """Implement HRRN scheduling."""
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
            
            # Calculate response ratio for each available process
            best_process = None
            best_ratio = -1
            
            for process in available:
                wait_time = current_time - process.arrival_time
                response_ratio = (wait_time + process.service_time) / process.service_time
                
                if response_ratio > best_ratio:
                    best_ratio = response_ratio
                    best_process = process
            
            # Execute the selected process to completion
            for t in range(current_time, current_time + best_process.service_time):
                if t < self.last_instant:
                    self.output.mark_executing(best_process.name, t)
                    self._mark_waiting_processes(t, best_process)
            
            current_time += best_process.service_time
            best_process.finish_time = current_time
            best_process.remaining_time = 0
            completed.append(best_process)
