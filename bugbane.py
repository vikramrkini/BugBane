import ast
import argparse
import copy
import sys
sys.path.append('/Users/vikramkini/CS527/project/bugbane/ansible-devel/lib/ansible')
import subprocess
import os
import re
import time
import astor
import random

# from operators import MutationOperator,ArithmeticOperatorMutationOperator,NegateBooleanMutationOperator,ReplaceStringMutationOperator,RemoveUnaryOperatorMutationOperator,ReplaceIntegerMutationOperator,ReplaceVariableMutationOperator,ReturnValuesMutator,InvertNegativesMutator,LogicalOperatorMutationOperator,ComparisonOperatorMutationOperator,IncrementsMutator,MathMutator,NegateConditionalsMutator, EmptyReturnsMutator
from operators import Return, MutationOperator, ConditionalsBoundaryMutator, IncrementsMutator, InvertNegativesMutator, MathMutator, NegateConditionalsMutator, VoidMethodCallMutator, FalseReturnsMutator, TrueReturnsMutator, NullReturnsMutator,RemoveConditionalsMutator
def get_mutant_filename(original_filename, mutant_index):
    return f"{original_filename[:-3]}mutant{mutant_index}.py"


def get_mutant_test_filename(original_filename, mutant_index):
    return f"{original_filename[:-3]}mutant{mutant_index}-test.py"

# def apply_mutations_to_file(filename, mutation_operators):
#     with open(filename, 'r') as f:
#         code = f.read()
  
#     original_tree = ast.parse(code)
#     mutants = []
#     # print(original_tree)
#     for mutation_operator in mutation_operators:
#         # print(mutation_operator.target_type)
#         if not isinstance(mutation_operator, MutationOperator):
#             raise TypeError("All mutation operators must be of type MutationOperator.")

#         if mutation_operator.target_type is None:
#             raise ValueError("All mutation operators must define a target_type attribute.")

#         for node_to_replace in ast.walk(original_tree):
#             # print(node_to_replace)
#             if not isinstance(node_to_replace, mutation_operator.target_type):
#                 # print(node_to_replace._fields)
#                 continue
#             # print(node_to_replace)
#             for mutated_node in mutation_operator.mutate_node(node_to_replace):
#                 mutated_tree = copy.deepcopy(original_tree)
#                 # print(mutated_node)
#                 for node in ast.walk(mutated_tree):
#                     # print(node)
#                     # if node is mutated_node and isinstance(node, ast.AST):
#                     if isinstance(node, ast.AST):
#                         # print('Node')
#                         node_to_replace.__dict__.update(mutated_node.__dict__)
#                         try :
#                             mutant_code = ast.unparse(mutated_tree)
#                         except KeyError as k :
#                             pass
#                         # print(mutant_code)
#                         mutant_filename = get_mutant_filename(filename, len(mutants))
#                         # print(mutant_filename)
#                         with open(mutant_filename, 'w') as f:
#                             f.write(mutant_code)

#                         mutants.append(mutant_filename)
#                         break

#     return mutants

import random

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
            result = subprocess.run(["pytest" ,test_file], cwd=test_dir, env=os.environ.copy())
        print(result)
    except Exception as e:
        print(f"Error running tests: {e}")
        # return False

    # If no exception is raised, assume all tests passed
    # if result.returncode == 0:
    #     return True
    # else:
    #     return False
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
    
    return parser

def list_mutation_operators(mutation_operators):
    print('---------------------------------------------------------------------------------')
    for mutation_operator in mutation_operators:
        print(type(mutation_operator).__name__ + ':')
        print('---------------------------------------------------------------------------------')
        print(" ")
        print(mutation_operator.__doc__)
        print('---------------------------------------------------------------------------------')

    


def run_bugbane(parser):
    
    mutation_operators = [  
        MathMutator(),
        ConditionalsBoundaryMutator(),
        IncrementsMutator(),
        InvertNegativesMutator(),
        NegateConditionalsMutator(),
        VoidMethodCallMutator(),
        FalseReturnsMutator(),
        TrueReturnsMutator(),
        # NullReturnsMutator(),
        RemoveConditionalsMutator()
        ]

    config = parser.parse_args()

    if config.list_operators:
        list_mutation_operators(mutation_operators)
        
    if config.source_file and config.test_file:
        start_time = time.time()
        # Extract the folder containing the source file path
        source_folder_path = os.path.abspath(config.source_file[0])
        source_folder_path = os.path.dirname(source_folder_path)
        original_filename = os.path.basename(config.source_file[0])
        test_folder_path = os.path.abspath(config.test_file[0])
        test_folder_path = os.path.dirname(test_folder_path)
        test_filename = os.path.basename(config.test_file[0])
        # Change the working directory to the folder containing the source file
        print(source_folder_path)
        os.chdir(source_folder_path)
        # Open the source code file
        
        # original_filename = config.source_file[0]
        # test_filename = config.test_file[0]
        print(original_filename,test_filename)
        mutants = apply_mutations_to_file(source_folder_path+'/'+original_filename,mutation_operators,config.num_mutants)
        # test_mutants = generate_mutant_test_files(original_filename,test_filename,mutants)
        number_of_mutants = len(mutants)
        number_of_test_failed = 0
        number_of_test_passed = 0
        print(source_folder_path+'/'+original_filename,test_folder_path+'/'+test_filename)
        
        copied_file = create_file_copy(source_folder_path+'/'+original_filename)  
        if not config.py_test:
            for index in range(number_of_mutants):
                load_file(source_folder_path+'/'+original_filename,mutants[index])
                if run_file_against_tests(source_folder_path+'/'+original_filename,test_folder_path+'/'+test_filename,True):
                    number_of_test_passed += 1
                else:
                    number_of_test_failed += 1
                # break
        else :
            for index in range(number_of_mutants):
                
                load_file(source_folder_path+'/'+original_filename,mutants[index])
                if run_file_against_tests(source_folder_path+'/'+original_filename,test_folder_path+'/'+test_filename,False):
                    number_of_test_passed += 1
                else:
                    number_of_test_failed += 1
                
                
        
        original_filename = load_file(original_filename,copied_file)
        
        print("Number of Mutants Passed: ",number_of_test_passed)
        print("Number of Mutants Failed: ",number_of_test_failed)
        print("Mutation Score: ", (number_of_test_failed/number_of_mutants)*100)
        # run_file_against_tests(original_filename,mutants,test_filename)
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Print the elapsed time in minutes and seconds
        print("Elapsed time: %d minutes %d seconds" % (elapsed_time // 60, elapsed_time % 60))
        
        if not config.show_mutants:
        # Remove mutated files and modified test files
            for mutant_filename in mutants:
                os.remove(mutant_filename)
                modified_test_filename = f"{test_filename}-mutant"
                if os.path.exists(modified_test_filename):
                    os.remove(modified_test_filename)
        os.remove(original_filename[:-3] + '-copy.py')
        # for mutant_test_filename in test_mutants:
        #     os.remove(mutant_test_filename)
        #     modified_test_filename = f"{test_filename}-mutant-test"
        #     if os.path.exists(modified_test_filename):
        #         os.remove(modified_test_filename)
        #  Remove the folder for mutated files
        # basename = os.path.basename(original_filename)
        # dirname = os.path.dirname(original_filename)
        # mutant_folder = os.path.join(dirname, basename + '_mutants')
        # shutil.rmtree(mutant_folder)

if __name__ == '__main__':
    parser = build_parser()
    run_bugbane(parser)

    