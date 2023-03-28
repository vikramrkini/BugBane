import ast
import argparse
import copy
import inspect
import sys
import subprocess
import os
import re
import shutil
import unittest
from unittest.mock import patch
import math
import importlib.util
from operators import MutationOperator,ArithmeticOperatorMutationOperator,NegateBooleanMutationOperator,ReplaceStringMutationOperator,RemoveUnaryOperatorMutationOperator,ReplaceIntegerMutationOperator,ReplaceVariableMutationOperator,ReturnValuesMutator,InvertNegativesMutator,LogicalOperatorMutationOperator,ComparisonOperatorMutationOperator,IncrementsMutator,MathMutator,NegateConditionalsMutator, EmptyReturnsMutator

def get_mutant_filename(original_filename, mutant_index):
    return f"{original_filename[:-3]}mutant{mutant_index}.py"
# def get_mutant_filename(filename, mutant_num):
#     basename = os.path.basename(filename)
#     dirname = os.path.dirname(filename)
#     mutant_folder = os.path.join(dirname, basename[:-3] + '_mutants')
#     os.makedirs(mutant_folder, exist_ok=True)
#     mutant_filename = os.path.join(mutant_folder, f"{basename[:-3]}-mutant{mutant_num}.py")
#     return mutant_filename

def get_mutant_test_filename(original_filename, mutant_index):
    return f"{original_filename[:-3]}mutant{mutant_index}-test.py"

def apply_mutations_to_file(filename, mutation_operators):
    with open(filename, 'r') as f:
        code = f.read()
  
    original_tree = ast.parse(code)
    mutants = []
    # print(original_tree)
    for mutation_operator in mutation_operators:
        # print(mutation_operator.target_type)
        if not isinstance(mutation_operator, MutationOperator):
            raise TypeError("All mutation operators must be of type MutationOperator.")

        if mutation_operator.target_type is None:
            raise ValueError("All mutation operators must define a target_type attribute.")

        for node_to_replace in ast.walk(original_tree):
            # print(node_to_replace)
            if not isinstance(node_to_replace, mutation_operator.target_type):
                # print(node_to_replace._fields)
                continue
            # print(node_to_replace)
            for mutated_node in mutation_operator.mutate_node(node_to_replace):
                mutated_tree = copy.deepcopy(original_tree)
                # print(mutated_node)
                for node in ast.walk(mutated_tree):
                    # print(node)
                    # if node is mutated_node and isinstance(node, ast.AST):
                    if isinstance(node, ast.AST):
                        # print('Node')
                        node_to_replace.__dict__.update(mutated_node.__dict__)
                        try :
                            mutant_code = ast.unparse(mutated_tree)
                        except KeyError as k :
                            pass
                        # print(mutant_code)
                        mutant_filename = get_mutant_filename(filename, len(mutants))
                        # print(mutant_filename)
                        with open(mutant_filename, 'w') as f:
                            f.write(mutant_code)

                        mutants.append(mutant_filename)
                        break

    return mutants

def run_file_against_tests(source_file_path: str, test_file_path: str,original_file_path :str):
    # Load the source code module
   
    with open(test_file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'import' in line:
            print(line)

    source_module = importlib.import_module(source_file_path[:-3])

    # Load the test module
    test_module = unittest.defaultTestLoader.loadTestsFromName(test_file_path[:-3])
    print(test_module)
    # Create a TestRunner and run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(test_module)

    # Print the results
    print(result)

    # Check if all the tests passed or not
    if result.wasSuccessful():
        return True
    else:
        return False

def generate_mutant_test_files(original_file,test_file, mutants):
    test_mutants = []
    number_of_mutants = len(mutants)
    for mutant_idx in range(number_of_mutants):
        mutant_test_filename = get_mutant_test_filename(original_file,mutant_idx)
        output_file = open(mutant_test_filename, 'w')
        with open(test_file, 'r') as f:
            output_file.write(f.read())                            
        test_mutants.append(mutant_test_filename)
    for mutant_idx,test_mutant in enumerate(test_mutants):
        mutant_filename = get_mutant_filename(original_file,mutant_idx)
        with open(test_mutant, 'r') as f:
            lines = f.readlines()
        with open(test_mutant, 'w') as f:
            for line in lines:
                if original_file[:-3] in line :
                    line = line.replace(original_file[:-3],mutant_filename[:-3])
                f.write(line)       
    return test_mutants


def replace_import_statement(original_file ,test_file, mutant_file,reverse = False):
    with open(test_file, 'r') as f:
        lines = f.readlines()
    with open(test_file, 'w') as f:
        for line in lines:
           
            if 'from' in line or 'import' in line:
                
                if not reverse:
                    if original_file in line :
                        line = line.replace(original_file,mutant_file)
                        
                else:
                    if mutant_file in line :
                        print('True')
                        # print(original_file,mutant_file)
                        line = line.replace(mutant_file,'$')
                        line = line.replace('$',original_file)
                    
            f.write(line)

def build_parser():
    parser = argparse.ArgumentParser(description='Bugbane - A comprehensive Mutation Testing Tool for Python Source Code',
                                     fromfile_prefix_chars='@')
    
    parser.add_argument('--source-file', '-s', type=str, nargs='+', help='target module or package to mutate')
    parser.add_argument('--test-file', '-t', type=str, nargs='+',
                        help='test class, test method, module or package with unit tests for the target')
    
    parser.add_argument('--show-mutants', '-m', action='store_true', help='show all mutant source codes')
    
    parser.add_argument('--list-operators', '-l', action='store_true', help='list available mutation operators')
    return parser

def list_mutation_operators(mutation_operators):
    for mutation_operator in mutation_operators:
        print(type(mutation_operator).__name__)
    


def run_bugbane(parser):
    mutation_operators = [
        ArithmeticOperatorMutationOperator([ast.Add, ast.Sub, ast.Mult, ast.Div]),
        LogicalOperatorMutationOperator([ast.And, ast.Or, ast.Not]),
        ComparisonOperatorMutationOperator([ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn]),
        NegateBooleanMutationOperator(),
        RemoveUnaryOperatorMutationOperator(),
        ReplaceIntegerMutationOperator(42),
        ReplaceStringMutationOperator("world"),
        ReplaceVariableMutationOperator("x","y"),
        ReturnValuesMutator(),
        InvertNegativesMutator(),
        IncrementsMutator() ,
        MathMutator() ,
        NegateConditionalsMutator(),
        EmptyReturnsMutator()
    ]
    config = parser.parse_args()

    if config.list_operators:
        list_mutation_operators(mutation_operators)
    
    # if len(sys.argv) < 3:
    #     print("Usage: python mutant_tester.py <original_file> <test_file>")
    #     return

    # original_filename = sys.argv[1]
    # test_filename = sys.argv[2]

    
    if config.source_file and config.test_file:
        original_filename = config.source_file[0]
        test_filename = config.test_file[0]
        print(original_filename,test_filename)
        mutants = apply_mutations_to_file(original_filename, mutation_operators)
        test_mutants = generate_mutant_test_files(original_filename,test_filename,mutants)
        number_of_mutants = len(mutants)
        number_of_test_failed = 0
        number_of_test_passed = 0
        for index in range(number_of_mutants):  
            if run_file_against_tests(mutants[index],test_mutants[index],original_filename):
                number_of_test_passed += 1
            else:
                number_of_test_failed += 1
        print("Number of Mutants Passed: ",number_of_test_passed)
        print("Number of Mutants Failed: ",number_of_test_failed)
        print("Mutation Score: ", (number_of_test_failed/number_of_mutants)*100)

        if not config.show_mutants:
        # Remove mutated files and modified test files
            for mutant_filename in mutants:
                os.remove(mutant_filename)
                modified_test_filename = f"{test_filename}-mutant"
                if os.path.exists(modified_test_filename):
                    os.remove(modified_test_filename)
        for mutant_test_filename in test_mutants:
            os.remove(mutant_test_filename)
            modified_test_filename = f"{test_filename}-mutant-test"
            if os.path.exists(modified_test_filename):
                os.remove(modified_test_filename)
        #  Remove the folder for mutated files
        # basename = os.path.basename(original_filename)
        # dirname = os.path.dirname(original_filename)
        # mutant_folder = os.path.join(dirname, basename + '_mutants')
        # shutil.rmtree(mutant_folder)

if __name__ == '__main__':
    parser = build_parser()
    run_bugbane(parser)

    