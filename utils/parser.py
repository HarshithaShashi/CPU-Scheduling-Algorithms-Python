"""
Input parser for reading and parsing scheduling simulation input.
"""

import sys
from typing import List, Tuple
from .process import Process


class InputParser:
    """Handles parsing of input data for scheduling simulation."""
    
    def __init__(self):
        self.operation = ""  # "trace" or "stats"
        self.algorithms = []  # List of (algorithm_id, quantum) tuples
        self.last_instant = 0
        self.process_count = 0
        self.processes = []
    
    def parse_from_stdin(self):
        """Parse input from standard input."""
        lines = sys.stdin.read().strip().split('\n')
        self.parse_from_lines(lines)
    
    def parse_from_file(self, filename: str):
        """Parse input from a file."""
        with open(filename, 'r') as f:
            lines = f.read().strip().split('\n')
        self.parse_from_lines(lines)
    
    def parse_from_lines(self, lines: List[str]):
        """Parse input from a list of lines."""
        if len(lines) < 4:
            raise ValueError("Invalid input format: too few lines")
        
        # Line 1: Operation mode
        self.operation = lines[0].strip().lower()
        if self.operation not in ['trace', 'stats']:
            raise ValueError(f"Invalid operation: {self.operation}")
        
        # Line 2: Algorithms
        self._parse_algorithms(lines[1].strip())
        
        # Line 3: Last instant
        self.last_instant = int(lines[2].strip())
        
        # Line 4: Process count
        self.process_count = int(lines[3].strip())
        
        # Lines 5+: Processes
        if len(lines) < 4 + self.process_count:
            raise ValueError("Invalid input: not enough process definitions")
        
        self._parse_processes(lines[4:4 + self.process_count])
    
    def _parse_algorithms(self, algorithm_line: str):
        """Parse algorithm specifications."""
        self.algorithms = []
        for algo_str in algorithm_line.split(','):
            algo_str = algo_str.strip()
            if '-' in algo_str:
                # Algorithm with quantum (e.g., "2-4" for RR with q=4)
                algo_id, quantum_str = algo_str.split('-')
                self.algorithms.append((algo_id, int(quantum_str)))
            else:
                # Algorithm without quantum
                self.algorithms.append((algo_str, None))
    
    def _parse_processes(self, process_lines: List[str]):
        """Parse process definitions."""
        self.processes = []
        for line in process_lines:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 3:
                raise ValueError(f"Invalid process definition: {line}")
            
            name = parts[0]
            arrival_time = int(parts[1])
            service_or_priority = int(parts[2])
            
            # For Aging algorithm (8), third field is priority
            # For others, it's service time
            # We'll handle this distinction in the algorithm itself
            process = Process(
                name=name,
                arrival_time=arrival_time,
                service_time=service_or_priority,
                priority=service_or_priority  # Will be used only for Aging
            )
            self.processes.append(process)
    
    def get_process_by_name(self, name: str) -> Process:
        """Get a process by its name."""
        for process in self.processes:
            if process.name == name:
                return process
        raise ValueError(f"Process {name} not found")
    
    def __repr__(self):
        return (f"InputParser(operation={self.operation}, "
                f"algorithms={self.algorithms}, "
                f"processes={len(self.processes)})")
