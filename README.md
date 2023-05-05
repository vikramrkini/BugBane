# BugBane
BugBane is a comprehensive mutation testing framework for Python. It uses a variety of mutation operators to generate mutants of your source code and runs your test suite against these mutants to assess the quality of your tests. BugBane can help you identify weaknesses in your tests and improve your test suite's ability to catch bugs.

## Features
1. Wide range of mutation operators
2. Support for both unittest and pytest test runners
3. Mutant code preview option
4. HTML report generation
5. Command-line interface for easy configuration and execution


## Installation

Clone the repository and install the required packages:

```
git clone https://github.com/yourusername/BugBane.git
cd BugBane
```

## Usage
Run the script with the following command:

```
python bugbane.py [OPTIONS]
```

### Options

--source-file / -s: Target module or package to mutate (required)

--test-file / -t: Test class, test method, module, or package with unit tests for the target (required)

--show-mutants / -m: Show all mutant source codes

--list-operators / -l: List available mutation operators

--py-test / -p: Use PyTest as the runner

--num-mutants / -n: Number of mutants to generate (default: 10)

--exclude-operators / -x: Mutation operators to exclude

--report / -r: Generate an HTML report

## Example
To run BugBane on your Python source code with unittest:

```
python bugbane.py -s path/to/your/source.py -t path/to/your/test.py
```

To use pytest as the test runner:

```
python bugbane.py -s path/to/your/source.py -t path/to/your/test.py -p
```


## Mutation Operators

BugBane uses the following mutation operators to generate mutants:

1. MathMutator: Mutates arithmetic operators
2. ConditionalsBoundaryMutator: Mutates conditional operators
3. IncrementsMutator: Mutates increment/decrement operators
4. InvertNegativesMutator: Inverts negative numbers
5. NegateConditionalsMutator: Negates conditional expressions
6. VoidMethodCallMutator: Deletes method calls with no return value
7. FalseReturnsMutator: Replaces return values with False
8. TrueReturnsMutator: Replaces return values with True
9. NullReturnsMutator: Replaces return values with None
10. RemoveConditionalsMutator: Removes conditional statements
11. NotConditionMutator: Adds a not operator to conditions
12. BooleanInvertMutator: Inverts boolean literals
13. FunctionCallArgumentSwapMutator: Swaps function call arguments
14. BooleanOperatorMutator: Mutates boolean operators
15. BitwiseOperatorMutator: Mutates bitwise operators


## License
This project is licensed under the MIT License.