"""
First Come First Serve (FCFS) scheduling algorithm.
"""

from .base import SchedulerBase


class FCFS(SchedulerBase):
    """
    First Come First Serve scheduling algorithm.
    Processes are executed in the order they arrive.
    Non-preemptive: Once a process starts, it runs to completion.
    """
    
    def schedule(self):
        """Implement FCFS scheduling."""
        # Sort processes by arrival time
        ready_queue = sorted(self.processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        
        for process in ready_queue:
            # If CPU is idle, advance time to next process arrival
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # Execute the process
            for t in range(current_time, current_time + process.service_time):
                if t < self.last_instant:
                    self.output.mark_executing(process.name, t)
                    # Mark other arrived processes as waiting
                    self._mark_waiting_processes(t, process)
            
            # Update process completion time
            current_time += process.service_time
            process.finish_time = current_time
            process.remaining_time = 0
