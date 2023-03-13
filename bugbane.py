import ast
import copy
import sys
import subprocess
import os
import re
import shutil
import unittest
import importlib.util

class MutationOperator:
    def __init__(self):
        self.target_type = None

    def mutate_node(self, node):
        raise NotImplementedError()


class ArithmeticOperatorMutationOperator(MutationOperator):
    def __init__(self, operators):
        super().__init__()
        self.operators = operators
        self.target_type = ast.BinOp

    def mutate_node(self, node):
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)) and node.op.__class__ in self.operators:
            for op_class in self.operators:
                if node.op.__class__ != op_class:
                    mutated_node = copy.deepcopy(node)
                    mutated_node.op = op_class()
                    yield mutated_node


class LogicalOperatorMutationOperator(MutationOperator):
    def __init__(self, operators):
        super().__init__()
        self.operators = operators
        self.target_type = ast.BoolOp

    def mutate_node(self, node):
        if isinstance(node.op, (ast.And, ast.Or)) and node.op.__class__ in self.operators:
            for op_class in self.operators:
                if node.op.__class__ != op_class:
                    mutated_node = copy.deepcopy(node)
                    mutated_node.op = op_class()
                    yield mutated_node


class ComparisonOperatorMutationOperator(MutationOperator):
    def __init__(self, operators):
        super().__init__()
        self.operators = operators
        self.target_type = ast.Compare

    def mutate_node(self, node):
        for i, op in enumerate(node.ops):
            if isinstance(op, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn)) and op.__class__ in self.operators:
                for op_class in self.operators:
                    if op.__class__ != op_class:
                        mutated_node = copy.deepcopy(node)
                        mutated_node.ops[i] = op_class()
                        yield mutated_node

class NegateBooleanMutationOperator(MutationOperator):
     '''
     NegateBooleanMutationOperator - This operator will replace any boolean value with its negation. For example, True becomes False and False becomes True.
     '''
     def __init__(self):
         super().__init__()
         self.target_type = ast.NameConstant

     def mutate_node(self, node):
         if isinstance(node.value, bool):
             mutated_node = copy.deepcopy(node)
             mutated_node.value = not mutated_node.value
             yield mutated_node

class RemoveUnaryOperatorMutationOperator(MutationOperator):
     '''
     RemoveUnaryOperatorMutationOperator - This operator will remove any unary operator from the code. For example, -x becomes x.
     '''
     def __init__(self):
         super().__init__()
         self.target_type = ast.UnaryOp

     def mutate_node(self, node):
         if isinstance(node.op, ast.UAdd) or isinstance(node.op, ast.USub):
             mutated_node = node.operand
             yield mutated_node
class ReplaceIntegerMutationOperator(MutationOperator):
     '''
     ReplaceIntegerMutationOperator - This operator will replace any integer value with a different integer value. For example, 42 becomes 23.

     '''
     def __init__(self, replacement_value):
         super().__init__()
         self.replacement_value = replacement_value
         self.target_type = ast.Num

     def mutate_node(self, node):
         if isinstance(node.n, int):
             mutated_node = copy.deepcopy(node)
             mutated_node.n = self.replacement_value
             yield mutated_node

class ReplaceStringMutationOperator(MutationOperator):
     '''
     ReplaceStringMutationOperator - This operator will replace any string value with a different string value. For example, "hello" becomes "world".
     '''
     def __init__(self, replacement_value):
         super().__init__()
         self.replacement_value = replacement_value
         self.target_type = ast.Str

     def mutate_node(self, node):
         if isinstance(node.s, str):
             mutated_node = copy.deepcopy(node)
             mutated_node.s = self.replacement_value
             yield mutated_node

class ReplaceVariableMutationOperator(MutationOperator):
     '''
     ReplaceVariableMutationOperator - This operator will replace any variable name with a different variable name. For example, x becomes y.
     '''
     def __init__(self, original_name, replacement_name):
         super().__init__()
         self.original_name = original_name
         self.replacement_name = replacement_name
         self.target_type = ast.Name

     def mutate_node(self, node):
         if isinstance(node.id, str) and node.id == self.original_name:
             mutated_node = copy.deepcopy(node)
             mutated_node.id = self.replacement_name
             yield mutated_node

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




# def run_tests(test_filename, test_command):
#     # Run the tests using the specified command and capture the output
#     try:
#         output = subprocess.check_output(test_command.format(test_filename), shell=True, stderr=subprocess.STDOUT)
#     except subprocess.CalledProcessError as e:
#         output = e.output

#     # Print the output of the tests
#     print(output.decode())

#     # Check if any test failures occurred
#     if b'FAILED' in output:
#         return False
#     else:
#         return True

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

# def run_tests(test_file, mutant_file):
#     try:
#         result = subprocess.run(['python', '-m', 'unittest', mutant_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     except FileNotFoundError:
#         print("Error: could not find 'python' interpreter.")
#         return None

#     if result.returncode == 0:
#         print(f"{mutant_file}: Test suite passed.")
#         return True
#     else:
#         print(f"{mutant_file}: Test suite failed.")
#         print(result.stdout.decode('utf-8'))
#         print(result.stderr.decode('utf-8'))
#         return False


# def calculate_mutation_score(source_file_path, test_file_path , mutation_operators):
#     with open(source_file_path, 'r') as f:
#         source_code = f.read()

#     # Create a list to hold the number of mutants generated by each mutation operator
#     mutant_counts = [0] * len(mutation_operators)

#     # Apply each mutation operator to the source code
#     original_tree = ast.parse(source_code)
#     for mutation_operator in mutation_operators:
#         if not isinstance(mutation_operator, MutationOperator):
#             raise TypeError("All mutation operators must be of type MutationOperator.")

#         if mutation_operator.target_type is None:
#             raise ValueError("All mutation operators must define a target_type attribute.")

#         for node_to_replace in ast.walk(original_tree):
#             if not isinstance(node_to_replace, mutation_operator.target_type):
#                 continue

#             # Generate the mutated code
#             for mutated_node in mutation_operator.mutate_node(node_to_replace):
#                 mutated_tree = copy.deepcopy(original_tree)
#                 ast.copy_location(mutated_node, node_to_replace)
#                 mutated_node_parent = next(ast.iter_parent_nodes(mutated_tree, node_to_replace))
#                 index = mutated_node_parent._fields.index(node_to_replace.__class__.__name__.lower())
#                 setattr(mutated_node_parent, mutated_node_parent._fields[index], mutated_node)
#                 mutated_code = ast.unparse(mutated_tree)

#                 # Write the mutated code to a temporary file
#                 with open('temp.py', 'w') as f:
#                     f.write(mutated_code)

#                 # Run the test suite on the mutated code
#                 result = subprocess.run(['python', test_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#                 # Check if the test suite failed
#                 if result.returncode != 0:
#                     mutant_counts[mutation_operators.index(mutation_operator)] += 1

#     # Calculate the mutation score
#     total_mutants = sum(mutant_counts)
#     mutation_score = (total_mutants / (len(mutation_operators) * ast.iter_child_nodes(original_tree).__length_hint__())) * 100

#     return mutation_score



def calculate_mutation_score(src_file, test_file, mutants):
    num_killed = 0
    for mutant in mutants:
        # Run test on mutant
        mutant = re.sub('\.mutant\d+','',mutant)
        result = subprocess.run(['python', test_file, mutant], capture_output=True)
        # Check if mutant was killed by the test
        if result.returncode != 0:
            num_killed += 1
    # print(num_killed)
    # print(len(mutants))
    mutation_score = num_killed / len(mutants)
    return mutation_score



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

#     # Run the tests and print the output
#     loader = unittest.TestLoader()
#     suite = loader.loadTestsFromModule(test_module)
#     runner = unittest.TextTestRunner()
#     result = runner.run(suite)
#     for test, output in result.failures + result.errors:
#         print(f"Output of {test}:\n{output}")

def run_tests(mutant_file, test_file,mutants):
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
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Calculate mutation score
    total_mutants = len(mutants)
    killed_mutants = total_mutants - len(result.failures) - len(result.errors)
    mutation_score = (killed_mutants / total_mutants) * 100

    # Print the mutation score and output of failed tests
    print(f"Mutation score: {mutation_score:.2f}%")
    for test, output in result.failures + result.errors:
        print(f"Output of {test}:\n{output}")



def run_bugbane():
    if len(sys.argv) < 3:
        print("Usage: python mutant_tester.py <original_file> <test_file>")
        return

    original_filename = sys.argv[1]
    test_filename = sys.argv[2]

    mutation_operators = [
        ArithmeticOperatorMutationOperator([ast.Add, ast.Sub, ast.Mult, ast.Div]),
        LogicalOperatorMutationOperator([ast.And, ast.Or, ast.Not]),
        ComparisonOperatorMutationOperator([ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn]),
        NegateBooleanMutationOperator(),
        RemoveUnaryOperatorMutationOperator(),
        ReplaceIntegerMutationOperator(42),
        ReplaceStringMutationOperator("world"),
    ]

    mutants = apply_mutations_to_file(original_filename, mutation_operators)

    for mutant_filename in mutants:
        print(mutant_filename,original_filename)
        replace_import_statement(original_filename[:-3],test_filename,mutant_filename[:-3])
        # modified_test_filename = modify_test_file(test_filename, original_filename, mutant_filename)
        
        run_tests(mutant_filename,test_filename,mutants)
        # if run_tests(mutant_filename,test_filename):
        #     print(f"{mutant_filename}: Test suite passed.")
        # else:
        #     print(f"{mutant_filename}: Test suite failed.")
        replace_import_statement(mutant_filename[:-3],test_filename,original_filename[:-3],reverse = True)
        # replace_import_statement(test_filename,original_filename)
       

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

