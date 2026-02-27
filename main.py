#!/usr/bin/env python3
"""
CPU Scheduling Algorithms Simulator
Main entry point for the scheduling simulation.
"""

import sys
from utils import InputParser, OutputFormatter
from algorithms import (FCFS, RoundRobin, SPN, SRT, HRRN, FB1, FB2i, Aging)


def get_algorithm_name(algo_id: str, quantum=None) -> str:
    """Get display name for an algorithm."""
    names = {
        '1': 'FCFS',
        '2': f'RR-{quantum}' if quantum else 'RR',
        '3': 'SPN',
        '4': 'SRT',
        '5': 'HRRN',
        '6': 'FB-1',
        '7': 'FB-2i',
        '8': f'Aging' if not quantum else f'Aging-{quantum}'
    }
    return names.get(algo_id, f'Unknown-{algo_id}')


def create_scheduler(algo_id: str, quantum, processes, last_instant, output_formatter):
    """Factory function to create appropriate scheduler."""
    if algo_id == '1':
        return FCFS(processes, last_instant, output_formatter)
    elif algo_id == '2':
        if quantum is None:
            quantum = 1
        return RoundRobin(processes, last_instant, output_formatter, quantum)
    elif algo_id == '3':
        return SPN(processes, last_instant, output_formatter)
    elif algo_id == '4':
        return SRT(processes, last_instant, output_formatter)
    elif algo_id == '5':
        return HRRN(processes, last_instant, output_formatter)
    elif algo_id == '6':
        return FB1(processes, last_instant, output_formatter)
    elif algo_id == '7':
        return FB2i(processes, last_instant, output_formatter)
    elif algo_id == '8':
        if quantum is None:
            quantum = 1
        return Aging(processes, last_instant, output_formatter, quantum)
    else:
        raise ValueError(f"Unknown algorithm ID: {algo_id}")


def main():
    """Main function."""
    try:
        # Parse input
        parser = InputParser()
        parser.parse_from_stdin()
        
        # Run each requested algorithm
        for algo_id, quantum in parser.algorithms:
            # Create output formatter
            output_formatter = OutputFormatter(parser.last_instant, parser.processes)
            
            # Create and run scheduler
            algo_name = get_algorithm_name(algo_id, quantum)
            try:
                scheduler = create_scheduler(algo_id, quantum, parser.processes, 
                                            parser.last_instant, output_formatter)
                scheduler.run()
                
                # Display results
                if parser.operation == 'trace':
                    output_formatter.print_trace(algo_name)
                elif parser.operation == 'stats':
                    output_formatter.print_stats(algo_name)
                
                print()  # Blank line between algorithms
                
            except NotImplementedError as e:
                print(f"Note: {e}", file=sys.stderr)
                continue
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
