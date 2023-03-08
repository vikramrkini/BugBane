import ast
import copy
import sys
import subprocess

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


def calculate_mutation_score(original_tests, mutants):
    num_total_mutants = len(mutants)
    num_killed_mutants = 0
    
    for mutant_file in mutants:
        # Run each mutant using the original test cases
        result = subprocess.run(['python', mutant_file], capture_output=True)
        mutant_output = result.stdout.decode('utf-8')
        
        # Check if any of the original test cases kill the mutant (i.e., produce different output)
        for test in original_tests:
            test_result = subprocess.run(['python', test], input=result.stdout, capture_output=True)
            if test_result.stdout.decode('utf-8') != mutant_output:
                num_killed_mutants += 1
                break
    print(num_killed_mutants,num_total_mutants)
    mutation_score = (num_killed_mutants / num_total_mutants) * 100
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
        ComparisonOperatorMutationOperator([ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn])
    ]
  
    mutants = apply_mutations_to_file(original_filename, mutation_operators)
    mutation_score = calculate_mutation_score(test_filename, mutants)
    print('Mutation score:', mutation_score)
    # # print(mutants)
    # for mutant_filename in mutants:
    #     if run_tests(test_filename,'python -m unittest {}'):
    #         print(f"{mutant_filename}: Test suite passed.")
    #     else:
    #         print(f"{mutant_filename}: Test suite failed.")

if __name__ == '__main__':
    run_bugbane()