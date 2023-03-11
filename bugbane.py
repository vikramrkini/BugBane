import ast
import copy
import sys
import subprocess
import os
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
    return f"{original_filename}.mutant{mutant_index}"


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




def run_tests(test_filename, test_command):
    # Run the tests using the specified command and capture the output
    try:
        output = subprocess.check_output(test_command.format(test_filename), shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Print the output of the tests
    print(output.decode())

    # Check if any test failures occurred
    if b'FAILED' in output:
        return False
    else:
        return True


# def calculate_mutation_score(original_tests, mutants):
#     num_total_mutants = len(mutants)
#     num_killed_mutants = 0
    
#     for mutant_file in mutants:
#         # Run each mutant using the original test cases
#         result = subprocess.run(['python', mutant_file], capture_output=True)
#         mutant_output = result.stdout.decode('utf-8')
        
#         # Check if any of the original test cases kill the mutant (i.e., produce different output)
#         for test in original_tests:
#             test_result = subprocess.run(['python', test], input=result.stdout, capture_output=True)
#             if test_result.stdout.decode('utf-8') != mutant_output:
#                 num_killed_mutants += 1
#                 break
#     print(num_killed_mutants,num_total_mutants)
#     mutation_score = (num_killed_mutants / num_total_mutants) * 100
#     return mutation_score

# def run_bugbane():
#     if len(sys.argv) < 3:
#         print("Usage: python mutant_tester.py <original_file> <test_file>")
#         return

#     original_filename = sys.argv[1]
#     test_filename = sys.argv[2]

#     mutation_operators = [
#         ArithmeticOperatorMutationOperator([ast.Add, ast.Sub, ast.Mult, ast.Div]),
#         LogicalOperatorMutationOperator([ast.And, ast.Or, ast.Not]),
#         ComparisonOperatorMutationOperator([ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn])
#     ]
  
#     mutants = apply_mutations_to_file(original_filename, mutation_operators)
#     mutation_score = calculate_mutation_score(test_filename, mutants)
#     print('Mutation score:', mutation_score)
#     # print(mutants)
#     for mutant_filename in mutants:
#         if run_tests(test_filename,'python -m unittest {}'):
#             print(f"{mutant_filename}: Test suite passed.")
#         else:
#             print(f"{mutant_filename}: Test suite failed.")




def calculate_mutation_score(source_filename, test_filename, mutation_operators):
    # Compile the source code to bytecode
    compiled_filename = f"{source_filename}c"
    if os.path.exists(compiled_filename):
        os.remove(compiled_filename)
    subprocess.check_call(["python", "-m", "py_compile", source_filename])
    
    # Run the original test suite against the original code
    with open(test_filename, "r") as f:
        original_output = subprocess.check_output(["python", "-"], stdin=f, text=True, timeout=30, errors="ignore")
    
    # Iterate over the mutation operators and apply each one to the source code
    mutant_index = 0
    total_mutants = 0
    for mutation_operator in mutation_operators:
        with open(source_filename, "r") as f:
            source_code = f.read()
        source_tree = ast.parse(source_code)
        mutated_trees = mutation_operator.mutate_node(source_tree)
        for mutated_tree in mutated_trees:
            # Write the mutated code to a file
            mutant_filename = f"{source_filename}_{mutant_index}.py"
            with open(mutant_filename, "w") as f:
                f.write(ast.unparse(mutated_tree))
            mutant_index += 1
        total_mutants += len(mutated_trees)
    
    # Run the original test suite against each mutant and count the killed mutants
    killed_mutants = 0
    for mutant_index in range(total_mutants):
        mutant_filename = f"{source_filename}_{mutant_index}.py"
        # Compile the mutant code to bytecode
        mutant_compiled_filename = f"{mutant_filename}c"
        if os.path.exists(mutant_compiled_filename):
            os.remove(mutant_compiled_filename)
        subprocess.check_call(["python", "-m", "py_compile", mutant_filename])
        # Run the test suite against the mutant code
        with open(test_filename, "r") as f:
            mutant_output = subprocess.check_output(["python", "-"], stdin=f, text=True, timeout=30, errors="ignore")
        # Compare the output of the test suite for the original code and the mutant code
        if mutant_output != original_output:
            killed_mutants += 1
        # Remove the compiled mutant code
        os.remove(mutant_compiled_filename)
        # Remove the mutated code file
        os.remove(mutant_filename)
    
    # Remove the compiled original code
    os.remove(compiled_filename)
    
    mutation_score = killed_mutants / total_mutants
    return mutation_score




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
    print(mutants)

    for mutant_filename in mutants:
        if run_tests(test_filename,'python -m unittest {}'):
            print(f"{mutant_filename}: Test suite passed.")
        else:
            print(f"{mutant_filename}: Test suite failed.")
    # score = calculate_mutation_score(original_filename, test_filename, mutation_operators)
    # print(score)
if __name__ == '__main__':
    run_bugbane()