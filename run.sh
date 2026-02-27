#!/bin/bash

# CPU Scheduling Algorithms - Run Script for Linux/WSL
# This script helps run the scheduling simulator easily

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  Fedora: sudo dnf install python3"
    echo "  Arch: sudo pacman -S python"
    exit 1
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTCASES_DIR="$PROJECT_DIR/testcases"

# Function to run a single test case
run_test() {
    local input_file=$1
    local filename=$(basename "$input_file")
    
    echo -e "${CYAN}========================================${NC}"
    echo -e "${YELLOW}Testing: $filename${NC}"
    echo -e "${CYAN}========================================${NC}"
    
    if [ -f "$input_file" ]; then
        python3 "$PROJECT_DIR/main.py" < "$input_file"
        echo ""
    else
        echo -e "${RED}Error: File not found: $input_file${NC}"
        return 1
    fi
}

# Function to run all test cases
run_all_tests() {
    echo -e "${GREEN}Running all test cases...${NC}\n"
    
    local count=0
    for input_file in "$TESTCASES_DIR"/*-input.txt; do
        if [ -f "$input_file" ]; then
            run_test "$input_file"
            ((count++))
        fi
    done
    
    echo -e "${GREEN}Completed $count test cases${NC}"
}

# Function to compare output with expected
compare_output() {
    local input_file=$1
    local output_file="${input_file%-input.txt}-output.txt"
    
    if [ ! -f "$output_file" ]; then
        echo -e "${YELLOW}Warning: No expected output file found${NC}"
        return 1
    fi
    
    echo -e "${CYAN}Comparing with expected output...${NC}"
    
    local temp_output=$(mktemp)
    python3 "$PROJECT_DIR/main.py" < "$input_file" > "$temp_output"
    
    if diff -q "$temp_output" "$output_file" > /dev/null; then
        echo -e "${GREEN}✓ Output matches expected result${NC}"
        rm "$temp_output"
        return 0
    else
        echo -e "${RED}✗ Output differs from expected result${NC}"
        echo -e "${YELLOW}Differences:${NC}"
        diff "$temp_output" "$output_file" || true
        rm "$temp_output"
        return 1
    fi
}

# Function to display usage
show_usage() {
    echo "Usage: $0 [OPTION] [TESTCASE]"
    echo ""
    echo "Options:"
    echo "  all               Run all test cases"
    echo "  compare FILE      Run test and compare with expected output"
    echo "  list              List available test cases"
    echo "  help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 testcases/01a-input.txt    # Run specific test"
    echo "  $0 all                         # Run all tests"
    echo "  $0 compare testcases/01a-input.txt  # Compare output"
    echo "  $0 list                        # List test cases"
}

# Function to list test cases
list_testcases() {
    echo -e "${CYAN}Available test cases:${NC}\n"
    
    for input_file in "$TESTCASES_DIR"/*-input.txt; do
        if [ -f "$input_file" ]; then
            local filename=$(basename "$input_file")
            local testname="${filename%-input.txt}"
            
            # Read first few lines to show what's being tested
            local mode=$(sed -n '1p' "$input_file")
            local algos=$(sed -n '2p' "$input_file")
            
            echo -e "${YELLOW}$filename${NC}"
            echo "  Mode: $mode"
            echo "  Algorithms: $algos"
            echo ""
        fi
    done
}

# Main script logic
main() {
    cd "$PROJECT_DIR"
    
    if [ $# -eq 0 ]; then
        show_usage
        exit 0
    fi
    
    case "$1" in
        all)
            run_all_tests
            ;;
        compare)
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Please specify a test case file${NC}"
                show_usage
                exit 1
            fi
            run_test "$2"
            compare_output "$2"
            ;;
        list)
            list_testcases
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            if [ -f "$1" ]; then
                run_test "$1"
            else
                echo -e "${RED}Error: File not found: $1${NC}"
                show_usage
                exit 1
            fi
            ;;
    esac
}

# Run main function
main "$@"
