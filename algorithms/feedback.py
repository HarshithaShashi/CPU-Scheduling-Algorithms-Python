"""
Feedback scheduling algorithms (FB-1 and FB-2i).
"""

from collections import deque
from .base import SchedulerBase


class FeedbackBase(SchedulerBase):
    """Base class for Feedback scheduling algorithms."""
    
    def __init__(self, processes, last_instant, output_formatter, num_queues=3):
        super().__init__(processes, last_instant, output_formatter)
        self.num_queues = num_queues
        self.queues = [deque() for _ in range(num_queues)]
    
    def get_quantum(self, queue_level):
        """Get quantum for a given queue level. Override in subclasses."""
        raise NotImplementedError
    
    def schedule(self):
        """Implement Feedback scheduling."""
        current_time = 0
        completed = 0
        total_processes = len(self.processes)
        
        # Track process queue levels
        process_queue_level = {p: 0 for p in self.processes}
        
        process_index = 0
        processes_sorted = sorted(self.processes, key=lambda p: p.arrival_time)
        
        while completed < total_processes and current_time < self.last_instant:
            # Add newly arrived processes to highest priority queue (queue 0)
            while process_index < len(processes_sorted) and processes_sorted[process_index].arrival_time <= current_time:
                self.queues[0].append(processes_sorted[process_index])
                process_index += 1
            
            # Find highest priority non-empty queue
            process = None
            current_queue_level = None
            for level in range(self.num_queues):
                if self.queues[level]:
                    process = self.queues[level].popleft()
                    current_queue_level = level
                    break
            
            if process is None:
                # No process available, advance to next arrival
                if process_index < len(processes_sorted):
                    current_time = processes_sorted[process_index].arrival_time
                else:
                    break
                continue
            
            # Get quantum for current queue level
            quantum = self.get_quantum(current_queue_level)
            execution_time = min(quantum, process.remaining_time)
            
            # Execute process
            for t in range(execution_time):
                if current_time < self.last_instant:
                    self.output.mark_executing(process.name, current_time)
                    self._mark_waiting_processes(current_time, process)
                current_time += 1
                process.remaining_time -= 1
            
            # Check for new arrivals during execution
            while process_index < len(processes_sorted) and processes_sorted[process_index].arrival_time < current_time:
                self.queues[0].append(processes_sorted[process_index])
                process_index += 1
            
            # If process not finished, move to lower priority queue
            if process.remaining_time > 0:
                next_level = min(current_queue_level + 1, self.num_queues - 1)
                self.queues[next_level].append(process)
            else:
                process.finish_time = current_time
                completed += 1


class FB1(FeedbackBase):
    """
    Feedback scheduling with quantum = 1 for all queues.
    """
    
    def get_quantum(self, queue_level):
        """Return quantum of 1 for all queue levels."""
        return 1


class FB2i(FeedbackBase):
    """
    Feedback scheduling with quantum = 2^i for queue level i.
    """
    
    def get_quantum(self, queue_level):
        """Return quantum = 2^i for queue level i."""
        return 2 ** queue_level
