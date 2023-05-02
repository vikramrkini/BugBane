import ast
import argparse
import copy
import sys
# sys.path.append('/Users/vikramkini/CS527/project/bugbane/ansible-devel/lib/ansible')
import subprocess
import os
import re
import time
import astor
import random
from yattag import Doc

from report import generate_html_report
# from operators import MutationOperator,ArithmeticOperatorMutationOperator,NegateBooleanMutationOperator,ReplaceStringMutationOperator,RemoveUnaryOperatorMutationOperator,ReplaceIntegerMutationOperator,ReplaceVariableMutationOperator,ReturnValuesMutator,InvertNegativesMutator,LogicalOperatorMutationOperator,ComparisonOperatorMutationOperator,IncrementsMutator,MathMutator,NegateConditionalsMutator, EmptyReturnsMutator
from operators import Return, MutationOperator, ConditionalsBoundaryMutator, IncrementsMutator, InvertNegativesMutator, MathMutator, NegateConditionalsMutator, VoidMethodCallMutator, FalseReturnsMutator, TrueReturnsMutator, NullReturnsMutator,RemoveConditionalsMutator, NotConditionMutator , BooleanInvertMutator , StatementDeletionMutator ,IfStatementSwapMutator , FunctionCallArgumentSwapMutator , BooleanOperatorMutator, BitwiseOperatorMutator
def get_mutant_filename(original_filename, mutant_index):
    return f"{original_filename[:-3]}mutant{mutant_index}.py"


def get_mutant_test_filename(original_filename, mutant_index):
    return f"{original_filename[:-3]}mutant{mutant_index}-test.py"

def apply_mutations_to_file(filename, mutation_operators, num_mutants):
    with open(filename, 'r') as f:
        code = f.read()

    original_tree = ast.parse(code)
    mutants = []

    for i in range(num_mutants):
        mutated_tree = copy.deepcopy(original_tree)

        for mutation_operator in mutation_operators:
            if not isinstance(mutation_operator, MutationOperator):
                raise TypeError("All mutation operators must be of type MutationOperator.")
            if mutation_operator.target_type is None:
                raise ValueError("All mutation operators must define a target_type attribute.")

            nodes_to_mutate = [node for node in ast.walk(mutated_tree) if isinstance(node, mutation_operator.target_type)]
            if len(nodes_to_mutate) > 0:
                node_to_replace = random.choice(nodes_to_mutate)
                for mutated_node in mutation_operator.mutate_node(node_to_replace):
                    node_to_replace.__dict__.update(mutated_node.__dict__)
                    break

        mutant_code = ast.unparse(mutated_tree)
        mutant_filename = get_mutant_filename(filename, i+1)
        with open(mutant_filename, 'w') as f:
            f.write(mutant_code)
        mutants.append(mutant_filename)

    return mutants

def create_file_copy(input_file_path):
    # Read the contents of the input file
    with open(input_file_path, 'r') as f:
        file_contents = f.read()

    # Create a new file with the same contents as the input file
    output_file_path = os.path.splitext(input_file_path)[0] + '-copy.py'
    with open(output_file_path, 'w') as f:
        f.write(file_contents)

    return output_file_path


def load_file(original_file,mutant_file):
    with open(mutant_file, 'r') as target_file:
        target_content = target_file.read()
    with open(original_file, 'w') as source_file:
        source_file.write(target_content)
        source_file.flush()
    target_file.close()
    source_file.close()
    return original_file
 
def run_file_against_tests(source_file_path: str, test_file_path: str, unittest : bool):
    # Get the directory containing the source and test files
    source_dir = os.path.dirname(source_file_path)
    test_dir = os.path.dirname(test_file_path)
    test_file = os.path.basename(test_file_path)

    # Execute the test file in a subprocess with the correct environment
    try:
        if unittest:
            result = subprocess.run(["python", "-m", "unittest", test_file], cwd=test_dir, env=os.environ.copy())
        else:
            result = subprocess.run(["pytest", "--cache-clear",test_file], cwd=test_dir, env=os.environ.copy())
        print(result)
    except Exception as e:
        print(f"Error running tests: {e}")
        # return False
    if result.returncode != 0:
        print(result.returncode)
        return False
    else:
        return True


def build_parser():
    parser = argparse.ArgumentParser(description='Bugbane - A comprehensive Mutation Testing Tool for Python Source Code',
                                     fromfile_prefix_chars='@')
    
    parser.add_argument('--source-file', '-s', type=str, nargs='+', help='target module or package to mutate')
    parser.add_argument('--test-file', '-t', type=str, nargs='+',
                        help='test class, test method, module or package with unit tests for the target')
    
    parser.add_argument('--show-mutants', '-m', action='store_true', help='show all mutant source codes')
    
    parser.add_argument('--list-operators', '-l', action='store_true', help='list available mutation operators')
    parser.add_argument('--py-test', '-p', action='store_true', help='Uses PyTest as the runner')
    parser.add_argument('--num-mutants', '-n', type=int, default=10, help='number of mutants to generate')
    parser.add_argument('--exclude-operators', '-x', type=str, nargs='+', help='mutation operators to exclude')
    parser.add_argument('--report', '-r', action='store_true', help='generate an HTML report')
    return parser

def list_mutation_operators(mutation_operators):
    print('---------------------------------------------------------------------------------')
    for mutation_operator in mutation_operators:
        print(type(mutation_operator).__name__ + ':')
        print('---------------------------------------------------------------------------------')
        print(" ")
        print(mutation_operator.__doc__)
        print('---------------------------------------------------------------------------------')

def find_matching_test_file(source_file_path, test_files):
    """
    Given the path of a source file and a list of test file paths, returns the name of a test file that
    matches the source file. Returns None if no matching test file is found.
    """
    source_file_name = os.path.basename(source_file_path)
    for file_path in test_files:
        file_name = os.path.basename(file_path)
        if file_name.startswith("test_") and file_name.endswith(".py"):
            # with open(file_path, "r") as test_file:
            #     contents = test_file.read()
            #     if source_file_name in contents:
            #         return file_name
            if source_file_name == file_name.replace("test_",''):
                return file_name
    return None



def get_py_files(folder_path):
    """
    Returns a list of the Python files in the given folder and its subfolders.
    
    Parameters:
        folder_path (str): The path of the folder to search for Python files.
        
    Returns:
        A list of the Python files in the given folder and its subfolders.
    """
    py_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py') or not file.startswith('test'):
                py_files.append(os.path.join(root, file))
    return py_files

def run_bugbane(parser):
    
    all_mutation_operators = [  
        MathMutator(),
        ConditionalsBoundaryMutator(),
        IncrementsMutator(),
        InvertNegativesMutator(),
        NegateConditionalsMutator(),
        VoidMethodCallMutator(),
        FalseReturnsMutator(),
        TrueReturnsMutator(),
        NullReturnsMutator(),
        RemoveConditionalsMutator(),
        NotConditionMutator(),
        BooleanInvertMutator(),
        # StatementDeletionMutator(),
        IfStatementSwapMutator(), 
        FunctionCallArgumentSwapMutator(), 
        BooleanOperatorMutator(),
        BitwiseOperatorMutator()
    ]

    config = parser.parse_args()

    # Filter out the excluded mutation operators
    if config.exclude_operators:
        excluded_operator_names = set(config.exclude_operators)
        mutation_operators = [op for op in all_mutation_operators if type(op).__name__ not in excluded_operator_names]
    else:
        mutation_operators = all_mutation_operators

    if config.list_operators:
        list_mutation_operators(mutation_operators)
        
    if config.source_file and config.test_file:
        start_time = time.time()
        source_folder_path = os.path.abspath(config.source_file[0])
        test_folder_path = os.path.abspath(config.test_file[0])
        print(test_folder_path)
        original_files = get_py_files(source_folder_path)
        test_files = get_py_files(test_folder_path)
        # print(original_files)
        # print(test_files)
        number_of_test_failed = 0
        number_of_test_passed = 0
        total_number_of_mutants = 0
        for original_filename in original_files:
            test_filename = find_matching_test_file(original_filename, test_files)
            if test_filename:
                os.chdir(source_folder_path)
                mutants = apply_mutations_to_file(original_filename,mutation_operators,config.num_mutants)
                number_of_mutants = len(mutants)
                total_number_of_mutants += number_of_mutants
                copied_file = create_file_copy(original_filename)  
                if not config.py_test:
                    for index in range(number_of_mutants):
                        load_file(original_filename,mutants[index])
                        if run_file_against_tests(original_filename,test_folder_path+'/'+test_filename,True):
                            number_of_test_passed += 1
                        else:
                            number_of_test_failed += 1
                else :
                    for index in range(number_of_mutants):
                        load_file(original_filename,mutants[index])
                        if run_file_against_tests(original_filename,test_folder_path+'/'+test_filename,False):
                            number_of_test_passed += 1
                        else:
                            number_of_test_failed += 1
                
                original_filename = load_file(original_filename,copied_file)


                if not config.show_mutants:
                    for mutant_filename in mutants:
                        os.remove(mutant_filename)
                        modified_test_filename = f"{test_filename}-mutant"
                        if os.path.exists(modified_test_filename):
                            os.remove(modified_test_filename)
                os.remove(original_filename[:-3] + '-copy.py')

            else:
                print(f"\nTest file not found for {original_filename}")
                  
        print(f"\n{original_filename} -> {test_filename}")
        print("Number of Mutants Passed: ",number_of_test_passed)
        print("Number of Mutants Failed: ",number_of_test_failed)
        mutation_score = (number_of_test_failed/total_number_of_mutants)*100
        print("Mutation Score: ", (number_of_test_failed/total_number_of_mutants)*100)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: %d minutes %d seconds" % (elapsed_time // 60, elapsed_time % 60))

        if config.report:
            generate_html_report(number_of_mutants,number_of_test_passed,number_of_test_failed,mutation_score)

if __name__ == '__main__':
    parser = build_parser()
    run_bugbane(parser)

    