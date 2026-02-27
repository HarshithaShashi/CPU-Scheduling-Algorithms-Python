"""
Round Robin (RR) scheduling algorithm with time quantum.
"""

from collections import deque
from .base import SchedulerBase


class RoundRobin(SchedulerBase):
    """
    Round Robin scheduling algorithm.
    Processes are executed in circular order with a fixed time quantum.
    Preemptive: Processes are interrupted after their quantum expires.
    """
    
    def __init__(self, processes, last_instant, output_formatter, quantum):
        super().__init__(processes, last_instant, output_formatter)
        self.quantum = quantum
    
    def schedule(self):
        """Implement Round Robin scheduling."""
        ready_queue = deque()
        current_time = 0
        completed = 0
        total_processes = len(self.processes)
        
        # Track which processes have been added to queue
        process_index = 0
        processes_sorted = sorted(self.processes, key=lambda p: p.arrival_time)
        
        while completed < total_processes and current_time < self.last_instant:
            # Add newly arrived processes to queue
            while process_index < len(processes_sorted) and processes_sorted[process_index].arrival_time <= current_time:
                if processes_sorted[process_index].remaining_time > 0:
                    ready_queue.append(processes_sorted[process_index])
                process_index += 1
            
            if not ready_queue:
                # CPU idle - advance to next process arrival
                if process_index < len(processes_sorted):
                    current_time = processes_sorted[process_index].arrival_time
                else:
                    break
                continue
            
            # Get next process from queue
            process = ready_queue.popleft()
            
            # Execute for quantum or remaining time, whichever is smaller
            execution_time = min(self.quantum, process.remaining_time)
            
            for t in range(execution_time):
                if current_time < self.last_instant:
                    self.output.mark_executing(process.name, current_time)
                    self._mark_waiting_processes(current_time, process)
                current_time += 1
                process.remaining_time -= 1
            
            # Check for new arrivals during execution
            while process_index < len(processes_sorted) and processes_sorted[process_index].arrival_time < current_time:
                if processes_sorted[process_index].remaining_time > 0 and processes_sorted[process_index] not in ready_queue:
                    ready_queue.append(processes_sorted[process_index])
                process_index += 1
            
            # If process not finished, put back in queue
            if process.remaining_time > 0:
                ready_queue.append(process)
            else:
                process.finish_time = current_time
                completed += 1
