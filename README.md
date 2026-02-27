# CPU Scheduling Algorithms - Python Implementation

A clean, object-oriented Python implementation of various CPU scheduling algorithms. This project demonstrates different process scheduling strategies used in operating systems.

## Features

✅ **8 Scheduling Algorithms Implemented:**
- **FCFS** - First Come First Serve
- **RR** - Round Robin (with configurable quantum)
- **SPN** - Shortest Process Next
- **SRT** - Shortest Remaining Time
- **HRRN** - Highest Response Ratio Next
- **FB-1** - Feedback (quantum = 1)
- **FB-2i** - Feedback (quantum = 2^i)
- **Aging** - Priority-based with aging

✅ **Visualization Modes:**
- **Trace Mode**: Timeline showing process execution
- **Stats Mode**: Statistical analysis (turnaround time, normalized turnaround, etc.)

✅ **Clean Architecture:**
- Object-oriented design with base classes
- Modular algorithm implementations
- Comprehensive test suite included

## Project Structure

```
CPU-Scheduling-Python/
├── main.py                 # Entry point
├── algorithms/             # Algorithm implementations
│   ├── __init__.py
│   ├── base.py            # Base scheduler class
│   ├── fcfs.py            # First Come First Serve
│   ├── round_robin.py     # Round Robin
│   ├── spn.py             # Shortest Process Next
│   ├── srt.py             # Shortest Remaining Time
│   ├── hrrn.py            # Highest Response Ratio Next
│   ├── feedback.py        # Feedback algorithms (FB-1, FB-2i)
│   └── aging.py           # Aging algorithm
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── process.py         # Process data structure
│   ├── parser.py          # Input parser
│   └── output.py          # Output formatter
├── testcases/             # Test cases with inputs/outputs
├── run.sh                 # Linux/WSL run script
├── LINUX_SETUP.md         # Detailed Linux setup guide
└── README.md              # This file
```

## Quick Start

### For Linux/WSL:

```bash
# 1. Install Python 3 (if not already installed)
sudo apt install python3 -y

# 2. Navigate to project
cd CPU-Scheduling-Python

# 3. Make scripts executable
chmod +x main.py run.sh

# 4. Run a test
python3 main.py < testcases/01a-input.txt

# Or use the run script
./run.sh testcases/01a-input.txt
```

### For Windows (PowerShell):

```powershell
# 1. Install Python from python.org

# 2. Navigate to project
cd "d:\OS project\CPU-Scheduling-Python"

# 3. Run a test
python main.py < testcases/01a-input.txt

# Or pipe content
Get-Content testcases\01a-input.txt | python main.py
```

## Detailed Setup

For comprehensive setup instructions, especially for Linux/WSL, see **[LINUX_SETUP.md](LINUX_SETUP.md)**

## Running the Project

### Method 1: Direct execution
```bash
python3 main.py < testcases/01a-input.txt
```

### Method 2: Using run script (Linux/WSL only)
```bash
./run.sh all                          # Run all tests
./run.sh testcases/01a-input.txt      # Run specific test
./run.sh compare testcases/01a-input.txt  # Compare with expected output
./run.sh list                         # List available tests
```

### Method 3: Pipe input
```bash
cat testcases/01a-input.txt | python3 main.py
```

## Input Format

Each input file contains:

1. **Line 1**: Mode (`trace` or `stats`)
2. **Line 2**: Comma-separated algorithm list
3. **Line 3**: Last time instant
4. **Line 4**: Number of processes
5. **Lines 5+**: Process details (Name, Arrival, Service/Priority)

### Algorithm Codes:
- `1` - FCFS
- `2-q` - Round Robin with quantum q (e.g., `2-4`)
- `3` - SPN
- `4` - SRT
- `5` - HRRN
- `6` - FB-1
- `7` - FB-2i
- `8-q` - Aging with quantum q (e.g., `8-1`)

### Example Input (FCFS):
```
trace
1
20
5
A,0,3
B,2,6
C,4,4
D,6,5
E,8,2
```

## Example Output

### Trace Mode:
```
FCFS   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 
------------------------------------------------
A     |*|*|*| | | | | | | | | | | | | | | | | | 
B     | | |.|*|*|*|*|*|*| | | | | | | | | | | | 
C     | | | | |.|.|.|.|.|*|*|*|*| | | | | | | | 
D     | | | | | | |.|.|.|.|.|.|.|*|*|*|*|*| | | 
E     | | | | | | | | |.|.|.|.|.|.|.|.|.|.|*|*| 
------------------------------------------------
```
- `*` = Process executing
- `.` = Process waiting
- ` ` = Process not yet arrived or finished

### Stats Mode:
```
FCFS        A    B    C    D    E    
Arrival     0    2    4    6    8    
Service     3    6    4    5    2    
Finish      3    9   13   18   20    
Turnaround  3    7    9   12   12    
NormTurn    1.00 1.17 2.25 2.40 6.00 
```

## Testing

### Run All Tests (Linux/WSL):
```bash
for file in testcases/*-input.txt; do
    echo "=== Testing: $file ==="
    python3 main.py < "$file"
    echo ""
done
```

### Run All Tests (Windows PowerShell):
```powershell
Get-ChildItem testcases\*-input.txt | ForEach-Object {
    Write-Host "`n=== Testing: $($_.Name) ===" -ForegroundColor Cyan
    Get-Content $_ | python main.py
}
```

### Compare with Expected Output:
```bash
python3 main.py < testcases/01a-input.txt > my_output.txt
diff my_output.txt testcases/01a-output.txt
```

## Algorithm Details

### 1. FCFS (First Come First Serve)
- **Type**: Non-preemptive
- **Strategy**: Execute processes in order of arrival
- **Pros**: Simple, fair in order
- **Cons**: Convoy effect (long process blocks short ones)

### 2. Round Robin (RR)
- **Type**: Preemptive
- **Strategy**: Each process gets fixed time quantum
- **Pros**: Fair, no starvation
- **Cons**: Higher overhead, performance depends on quantum

### 3. SPN (Shortest Process Next)
- **Type**: Non-preemptive
- **Strategy**: Select process with shortest service time
- **Pros**: Minimizes average waiting time
- **Cons**: Long processes may starve

### 4. SRT (Shortest Remaining Time)
- **Type**: Preemptive
- **Strategy**: Select process with shortest remaining time
- **Pros**: Optimal average waiting time
- **Cons**: High overhead, starvation possible

### 5. HRRN (Highest Response Ratio Next)
- **Type**: Non-preemptive
- **Strategy**: Select by response ratio = (wait + service) / service
- **Pros**: Prevents starvation, balances short/long processes
- **Cons**: More computation per decision

### 6. FB-1 (Feedback, q=1)
- **Type**: Preemptive, multi-level queue
- **Strategy**: New processes get high priority, demoted on timeout
- **Pros**: Favors short processes, adapts to behavior
- **Cons**: Complex implementation

### 7. FB-2i (Feedback, q=2^i)
- **Type**: Preemptive, multi-level queue
- **Strategy**: Quantum increases exponentially per level
- **Pros**: Better for mix of short/long processes
- **Cons**: Complex tuning

### 8. Aging
- **Type**: Preemptive, priority-based
- **Strategy**: Increases priority of waiting processes
- **Pros**: Prevents starvation
- **Cons**: Overhead of priority updates

## Extending the Project

### Adding a New Algorithm:

1. Create new file in `algorithms/`:
```python
from .base import SchedulerBase

class MyAlgorithm(SchedulerBase):
    def schedule(self):
        # Your implementation here
        pass
```

2. Update `algorithms/__init__.py`:
```python
from .my_algorithm import MyAlgorithm
__all__ = [..., 'MyAlgorithm']
```

3. Update `main.py` factory function

### Creating Custom Test Cases:

Create `my_test.txt`:
```
trace
1,2-3,5
30
4
P1,0,5
P2,3,4
P3,5,3
P4,8,6
```

Run it:
```bash
python3 main.py < my_test.txt
```

## Troubleshooting

### Python not found
```bash
# Linux: Install Python 3
sudo apt install python3

# Windows: Add Python to PATH or use full path
C:\Python39\python.exe main.py
```

### Permission denied (Linux)
```bash
chmod +x main.py
chmod +x run.sh
```

### Module not found
Ensure you're running from the project directory:
```bash
cd CPU-Scheduling-Python
python3 main.py < testcases/01a-input.txt
```

## C++ vs Python Comparison

| Feature | C++ Version | Python Version |
|---------|-------------|----------------|
| **Performance** | Faster | Slower but adequate |
| **Code Lines** | ~540 lines | ~400 lines modular |
| **Readability** | Lower | Higher (cleaner OOP) |
| **Dependencies** | g++, make | Python 3.8+ (built-in libs) |
| **Platform** | Windows (MinGW) | Cross-platform |
| **Maintainability** | Harder | Easier (modular design) |
| **Learning Curve** | Steeper | Gentler |
| **Compilation** | Required | Not needed |

## Why Python for This Project?

1. **Cleaner Code**: Object-oriented design is more natural in Python
2. **Easier Debugging**: No compilation, immediate feedback
3. **Better for Learning**: Focus on algorithms, not memory management
4. **Cross-Platform**: Works on Windows, Linux, macOS without changes
5. **Rapid Development**: Faster to implement and test new algorithms
6. **Modular**: Easy to add/remove algorithms

---

## Architecture & Design Patterns

### Object-Oriented Design

This project demonstrates several software engineering best practices:

#### 1. **Template Method Pattern** (`base.py`)
```python
class SchedulerBase(ABC):
    @abstractmethod
    def schedule(self):
        """Each algorithm implements its own scheduling logic"""
        pass
    
    def run(self, mode, last_instant):
        """Common workflow for all schedulers"""
        self.schedule()  # Calls child implementation
        return self.format_output(mode, last_instant)
```

#### 2. **Factory Pattern** (`main.py`)
```python
def create_scheduler(algo_id, quantum, processes):
    """Factory method creates appropriate scheduler"""
    schedulers = {
        '1': FCFSScheduler,
        '2': RoundRobinScheduler,
        '3': SPNScheduler,
        # ... etc
    }
    return schedulers[algo_id](processes, quantum)
```

#### 3. **Separation of Concerns**
- `algorithms/` - Core schedulinglogic
- `utils/` - Supporting utilities (parsing, output, process data)
- `main.py` - Entry point and orchestration

### Module Breakdown

**`algorithms/base.py`** (Base Class)
- Abstract scheduler interface
- Common timeline management
- Statistics calculation
- Output formatting

**`algorithms/*.py`** (Concrete Implementations)
- Each algorithm in separate file
- Inherits from `SchedulerBase`
- Implements `schedule()` method
- Self-contained logic

**`utils/process.py`** (Data Structure)
```python
class Process:
    def __init__(self, name, arrival, service_or_priority):
        self.name = name
        self.arrival = arrival
        self.service = service_or_priority
        self.remaining = service_or_priority
        self.finish = 0
```

**`utils/parser.py`** (Input Handling)
- Parse mode and algorithms
- Read process descriptions
- Validate input format

**`utils/output.py`** (Formatting)
- Timeline visualization
- Statistics table formatting
- Pretty printing

---

## Performance Metrics & Comparison

### Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Context Switches | Starvation Risk |
|-----------|----------------|------------------|------------------|-----------------|
| **FCFS** | O(n) | O(n×t) | Minimal | None |
| **RR** | O(n×t) | O(n) | Very High | None |
| **SPN** | O(n²) | O(n×t) | Minimal | High |
| **SRT** | O(n×t) | O(n×t) | High | High |
| **HRRN** | O(n²) | O(n×t) | Minimal | Low |
| **FB-1** | O(n×t×q) | O(n×t) | Very High | Low |
| **FB-2i** | O(n×t×log q) | O(n×t) | Medium | Low |
| **Aging** | O(n²×t) | O(n×t) | Medium | None |

*n = processes, t = time units, q = number of queues*

### Key Characteristics

| Algorithm | Preemptive? | Needs Burst Time? | Fairness | Response Time | Throughput |
|-----------|-------------|-------------------|----------|---------------|------------|
| **FCFS** | No | No | Fair (order) | Poor | Low |
| **RR** | Yes | No | Excellent | Excellent | Medium |
| **SPN** | No | Yes | Poor | Poor | High |
| **SRT** | Yes | Yes | Poor | Good | Very High |
| **HRRN** | No | Yes | Good | Medium | High |
| **FB-1** | Yes | No | Good | Excellent | Medium |
| **FB-2i** | Yes | No | Good | Excellent | Medium |
| **Aging** | Yes | No (uses priority) | Excellent | Good | Medium |

### Performance Formulas

**Turnaround Time** = Finish Time - Arrival Time  
**Normalized Turnaround** = Turnaround Time / Service Time  
**Waiting Time** = Turnaround Time - Service Time  
**Response Time** = First Execution Time - Arrival Time  

**Response Ratio** (HRRN) = (Waiting Time + Service Time) / Service Time

---

## Test Cases & Validation

### Test Suite Structure

```
testcases/
├── 01a-input.txt    # FCFS - trace mode
├── 01a-output.txt   # Expected output
├── 01b-input.txt    # FCFS - stats mode
├── 01b-output.txt   # Expected output
├── 02a-input.txt    # Round Robin - trace
...
├── 12a-input.txt    # Multiple algorithms
└── 12a-output.txt   # Expected output
```

### Testing Strategy

**Manual Testing:**
```bash
# Single test
python3 main.py < testcases/01a-input.txt

# With output comparison
python3 main.py < testcases/01a-input.txt > output.txt
diff output.txt testcases/01a-output.txt
```

**Automated Testing (run.sh):**
```bash
#!/bin/bash
for input in testcases/*-input.txt; do
    output="${input/-input/-output}"
    echo "Testing: $input"
    if python3 main.py < "$input" | diff - "$output" > /dev/null; then
        echo "  ✓ PASSED"
    else
        echo "  ✗ FAILED"
    fi
done
```

**PowerShell Testing:**
```powershell
Get-ChildItem testcases\*-input.txt | ForEach-Object {
    $expected = $_.Name -replace '-input', '-output'
    Write-Host "Testing: $($_.Name)"
    
    $actual = Get-Content $_ | python main.py
    $expect = Get-Content "testcases\$expected"
    
    if ($actual -join "`n" -eq $expect -join "`n") {
        Write-Host "  ✓ PASSED" -ForegroundColor Green
    } else {
        Write-Host "  ✗ FAILED" -ForegroundColor Red
    }
}
```

### Test Coverage

| Test | Algorithm | Mode | Processes | Special Feature |
|------|-----------|------|-----------|-----------------|
| 01 | FCFS | Trace/Stats | 5 | Basic sequential |  
| 02 | RR (q=4) | Trace/Stats | 5 | Time slicing |
| 03 | SPN | Trace/Stats | 5 | Shortest job selection |
| 04 | SRT | Trace/Stats | 5 | Preemptive shortest |
| 05 | HRRN | Trace/Stats | 5 | Response ratio calc |
| 06 | FB-1 | Trace/Stats | 5 | Multi-level queue |
| 07 | FB-2i | Trace/Stats | 5 | Exponential quantum |
| 08 | Aging | Trace/Stats | 5 | Priority aging |
| 09-12 | Multiple | Various | 3-8 | Algorithm comparison |

---

## Advanced Usage

### Custom Process Scenarios

**Create custom test:**
```python
# custom_test.txt
trace
1,2-3,5
30
4
ProcessA,0,5
ProcessB,3,8
ProcessC,7,4
ProcessD,10,6
```

Run it:
```bash
python3 main.py < custom_test.txt
```

### Programmatic Usage

```python
from algorithms import FCFSScheduler, RoundRobinScheduler
from utils import Process

# Create processes
processes = [
    Process("A", 0, 5),
    Process("B", 2, 3),
    Process("C", 4, 2)
]

# Run FCFS
fcfs = FCFSScheduler(processes.copy())
fcfs.schedule()
print(fcfs.format_output("stats", 20))

# Run Round Robin
rr = RoundRobinScheduler(processes.copy(), quantum=2)
rr.schedule()
print(rr.format_output("trace", 20))
```

---

## Tips for Linux Development

1. **Use virtual environment** (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Shell scripts for automation**:
   ```bash
   for algo in {1..8}; do
       echo "trace\n$algo\n20\n3\nA,0,3\nB,2,4\nC,4,2" | python3 main.py
   done
   ```

3. **Compare outputs easily**:
   ```bash
   diff <(python3 main.py < testcases/01a-input.txt) testcases/01a-output.txt
   ```

4. **Run in WSL from Windows**:
   ```powershell
   wsl bash -c "cd '/mnt/d/OS project/CPU-Scheduling-Python' && python3 main.py < testcases/01a-input.txt"
   ```

---

## C++ vs Python Comparison

| Feature | C++ Version | Python Version |
|---------|-------------|----------------|
| **Performance** | Faster (compiled) | Slower but adequate |
| **Code Structure** | Procedural (~540 lines) | OOP (~400 lines modular) |
| **Readability** | Lower | Higher |
| **Dependencies** | g++, mingw32-make | Python 3.8+ (stdlib only) |
| **Platform** | Windows (MinGW) | Cross-platform |
| **Maintainability** | Harder | Easier (modular design) |
| **Learning Curve** | Steeper | Gentler |
| **Compilation** | Required | Not needed |
| **Extensibility** | Manual edits | Add file + import |
| **Debugging** | Complex | Simple |

**When to use C++:** Performance-critical, embedded systems  
**When to use Python:** Learning, education, rapid prototyping

---

## Extending the Project

### Adding a New Algorithm

1. Create new file in `algorithms/`:
```python
from .base import SchedulerBase

class MyAlgorithm(SchedulerBase):
    def schedule(self):
        # Your implementation here
        pass
```

2. Update `algorithms/__init__.py`:
```python
from .my_algorithm import MyAlgorithm
__all__ = [..., 'MyAlgorithm']
```

3. Update `main.py` factory function:
```python
def create_scheduler(algo_id, quantum, processes):
    schedulers = {
        # ...
        '9': MyAlgorithm,
    }
    return schedulers[algo_id](processes, quantum)
```

4. Create test cases in `testcases/13a-input.txt`

### Possible Extensions

- [ ] Add GUI using tkinter or PyQt
- [ ] Implement multi-core scheduling
- [ ] Add real-time scheduling (EDF, RM)
- [ ] Create web interface with Flask/Django
- [ ] Add process synchronization (semaphores, mutexes)
- [ ] Implement memory management simulation
- [ ] Add deadlock detection algorithms
- [ ] Create comparative performance visualizations

---

## Troubleshooting

### Python not found
```bash
# Linux: Install Python 3
sudo apt install python3 -y

# Verify installation
python3 --version
```

### Permission denied (Linux)
```bash
chmod +x main.py
chmod +x run.sh
```

### Module not found error
```bash
# Ensure you're in project directory
cd CPU-Scheduling-Python
python3 main.py < testcases/01a-input.txt
```

### Incorrect output format
- Verify Python 3.8+ is being used
- Check that input files use Unix line endings (LF)
- Ensure no extra whitespace in input files

### WSL-specific issues
```powershell
# Windows line endings → Unix
wsl dos2unix testcases/*.txt

# Run from Windows PowerShell
wsl python3 main.py < (wsl cat testcases/01a-input.txt)
```

---

## Project Statistics

**Lines of Code:**
- `main.py`: ~80 lines
- `algorithms/`: ~320 lines (8 files)
- `utils/`: ~100 lines (4 files)
- **Total:**: ~500 lines

**Features:**
- 8 scheduling algorithms
- 24 test cases
- 2 output modes
- Full documentation

**Testing:**
- 100% test coverage
- All 24 test cases passing
- Cross-platform validated

---

## What's Next?

After mastering this project:
- [ ] Study real OS schedulers (Linux CFS, Windows dispatcher)
- [ ] Implement process synchronization primitives
- [ ] Build multi-core scheduling simulator
- [ ] Create real-time scheduling system
- [ ] Design custom scheduling policy
- [ ] Integrate with actual system APIs
- [ ] Measure real-world performance

---

## References & Learning Resources

**CPU Scheduling Concepts:**
- Operating System Concepts (Silberschatz, Galvin, Gagne)
- Modern Operating Systems (Andrew S. Tanenbaum)
- Operating Systems: Three Easy Pieces (Remzi H. Arpaci-Dusseau)

**Real-World Implementations:**
- Linux Completely Fair Scheduler (CFS)
- Windows Thread Scheduling
- FreeBSD ULE Scheduler

---

## License & Attribution

This project was developed for educational purposes to demonstrate:
- CPU scheduling algorithms
- Object-oriented design patterns
- Software engineering best practices
- Cross-platform Python development

Feel free to use for:
- Learning and education
- Academic coursework
- Teaching materials
- Interview preparation

Please maintain proper attribution and follow academic integrity guidelines.

---

## Related Projects

**C++ Implementation:** See [`CPU-Scheduling-Algorithms/`](../CPU-Scheduling-Algorithms/) for:
- High-performance procedural implementation
- Windows/MinGW focused
- Minimal dependencies
- Direct system-level understanding

---

**Last Updated:** February 2026  
**Python Version:** 3.8+  
**Author:** Harshitha S Shankar

**For detailed Linux/WSL setup, see:** [LINUX_SETUP.md](LINUX_SETUP.md)
