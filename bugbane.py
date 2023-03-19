import ast
import copy
import inspect
import sys
import subprocess
import os
import re
import shutil
import unittest
import math
import importlib.util
from operators import MutationOperator,ArithmeticOperatorMutationOperator,NegateBooleanMutationOperator,ReplaceStringMutationOperator,RemoveUnaryOperatorMutationOperator,ReplaceIntegerMutationOperator,ReplaceVariableMutationOperator,ReturnValuesMutator,InvertNegativesMutator,LogicalOperatorMutationOperator,ComparisonOperatorMutationOperator,IncrementsMutator,MathMutator,NegateConditionalsMutator, EmptyReturnsMutator

def get_mutant_filename(original_filename, mutant_index):
    return f"{original_filename[:-3]}mutant{mutant_index}.py"

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
                        mutant_code = ast.unparse(mutated_tree)
                        # print(mutant_code)
                        mutant_filename = get_mutant_filename(filename, len(mutants))
                        # print(mutant_filename)
                        with open(mutant_filename, 'w') as f:
                            f.write(mutant_code)

                        mutants.append(mutant_filename)
                        break

    return mutants

def modify_test_file(test_filename, original_filename, mutant_filename):
    with open(test_filename, "r") as file:
        test_contents = file.read()

    mutant_name = os.path.splitext(os.path.basename(mutant_filename))[0]
    original_name = os.path.splitext(os.path.basename(original_filename))[0]
    modified_contents = test_contents.replace(original_name, mutant_name)

    modified_test_filename = f"{test_filename}.mutant"
    with open(modified_test_filename, "w") as file:
        file.write(modified_contents)

    return modified_test_filename

def replace_import_statement(original_file ,test_file, mutant_file,reverse = False):
    with open(test_file, 'r') as f:
        lines = f.readlines()
    with open(test_file, 'w') as f:
        for line in lines:
            if 'from ' in line or 'import' in line:
                if reverse:
                    if original_file in line :
                        line = line.replace(mutant_file,original_file)
                        print(line)
                else:
                    if mutant_file in line :
                        line = line.replace(original_file,mutant_file)
                        print(line)

            f.write(line)

# def run_tests(mutant_file, test_file):
#     # Load the test cases from the test file
#     spec = importlib.util.spec_from_file_location("test_module", test_file)
#     test_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(test_module)

#     # Load the mutant code as a module
#     spec = importlib.util.spec_from_file_location("mutant_module", mutant_file)
#     mutant_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(mutant_module)

#     # Run the tests and calculate the mutation score
#     loader = unittest.TestLoader()
#     suite = loader.loadTestsFromModule(test_module)
#     runner = unittest.TextTestRunner()
#     result = runner.run(suite)

#     print(result)
#     for test, output in result.failures + result.errors:
#         print(f"Output of {test}:\n{output}")
import importlib.util
import unittest
from unittest.mock import patch

def run_tests(mutant_file, test_file):
    # Load the test cases from the test file
    spec = importlib.util.spec_from_file_location("test_module", test_file)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    # Load the mutant code as a module
    spec = importlib.util.spec_from_file_location("mutant_module", mutant_file)
    mutant_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mutant_module)

    # Run the tests and calculate the mutation score
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)

    # Replace original code with mutant code using patch
    for func_name, func_obj in inspect.getmembers(mutant_module, inspect.isfunction):
        # print(func_name)
        with patch.object(test_module, func_name, side_effect=func_obj):
            pass

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    for test, output in result.failures + result.errors:
        print(f"Output of {test}:\n{output}")



def calculate_mutation_score(original_file, mutants, test_file):
    num_killed = 0
    for mutant in mutants:
        try:
            replace_import_statement(original_file[:-3],test_file,mutant[:-3])
            result = subprocess.run(["python", test_file], capture_output=True, check=True, text=True, input=f"{mutant}\n")
            if "FAILED" in result.stdout or "ERROR" in result.stdout:
                print(f"Mutant {mutant} killed by test file {test_file}")
                num_killed += 1
            else:
                print(f"Mutant {mutant} survived test file {test_file}")
            replace_import_statement(mutant[:-3],test_file,original_file[:-3],reverse = True)
        except subprocess.CalledProcessError:
            print(f"Error running test file {test_file} on mutant {mutant}")

    mutation_score = num_killed / len(mutants)
    return mutation_score




def run_bugbane():
    if len(sys.argv) < 3:
        print("Usage: python mutant_tester.py <original_file> <test_file>")
        return

    original_filename = sys.argv[1]
    test_filename = sys.argv[2]

    mutation_operators = [
        # ArithmeticOperatorMutationOperator([ast.Add, ast.Sub, ast.Mult, ast.Div]),
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

    mutants = apply_mutations_to_file(original_filename, mutation_operators)

    for mutant_filename in mutants:
        print(mutant_filename,original_filename)
        replace_import_statement(original_filename[:-3],test_filename,mutant_filename[:-3])
        # modified_test_filename = modify_test_file(test_filename, original_filename, mutant_filename)
        
        # run_tests(mutant_filename,test_filename,mutants)
        print(run_tests(mutant_filename,test_filename))

        # if run_tests(mutant_filename,test_filename):
        #     print(f"{mutant_filename}: Test suite passed.")
        # else:
        #     print(f"{mutant_filename}: Test suite failed.")
        replace_import_statement(mutant_filename[:-3],test_filename,original_filename[:-3],reverse = True)
        # replace_import_statement(test_filename,original_filename)
       
    # print(calculate_mutation_score(original_filename,mutants,test_filename))
    # score = calculate_mutation_score(original_filename, test_filename, mutants)
    # print(f"Mutation score: {score}")

    # Remove mutated files and modified test files
    for mutant_filename in mutants:
        os.remove(mutant_filename)
        modified_test_filename = f"{test_filename}-mutant"
        if os.path.exists(modified_test_filename):
            os.remove(modified_test_filename)

if __name__ == '__main__':
    run_bugbane()

