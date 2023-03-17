import ast
import copy
import math

#### This file contains all the operators defined in Bugbane.

class MutationOperator:
    def __init__(self):
        self.target_type = None

    def mutate_node(self, node):
        raise NotImplementedError()

class MathMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.BinOp

    def mutate_node(self, node):
        if isinstance(node, self.target_type):
            mutated_node = ast.copy_location(ast.parse(self.get_mutation(node)), node)
            yield mutated_node.body[0].value

    def get_mutation(self, node):
        operator = node.op.__class__
        operator_map = {
            ast.Add: ast.Sub,
            ast.Sub: ast.Add,
            ast.Mult: ast.Div,
            ast.Div: ast.Mult,
            ast.Mod: ast.Mult,
            ast.BitAnd: ast.BitOr,
            ast.BitOr: ast.BitAnd,
            ast.BitXor: ast.BitAnd,
            ast.LShift: ast.RShift,
            ast.RShift: ast.LShift,
            ast.FloorDiv: ast.Mult,
            ast.Pow : ast.Pow
        }
        new_operator = operator_map[operator]
        mutation_str = ast.dump(ast.fix_missing_locations(ast.BinOp(node.left, new_operator(), node.right)))
        return mutation_str


class NegateConditionalsMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Compare

    def mutate_node(self, node):
        if isinstance(node, ast.Compare):
            mutated_node = copy.deepcopy(node)
            if isinstance(node.ops[0], ast.Eq):
                mutated_node.ops[0] = ast.NotEq()
            elif isinstance(node.ops[0], ast.NotEq):
                mutated_node.ops[0] = ast.Eq()
            elif isinstance(node.ops[0], ast.LtE):
                mutated_node.ops[0] = ast.Gt()
            elif isinstance(node.ops[0], ast.GtE):
                mutated_node.ops[0] = ast.Lt()
            elif isinstance(node.ops[0], ast.Lt):
                mutated_node.ops[0] = ast.GtE()
            elif isinstance(node.ops[0], ast.Gt):
                mutated_node.ops[0] = ast.LtE()
            yield mutated_node


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

class InvertNegativesMutator(MutationOperator):
    '''
    The invert negatives mutator inverts negation of integer and floating point variables.
    '''
    def __init__(self):
        super().__init__()
        self.target_type = ast.UnaryOp

    def mutate_node(self, node):
        if isinstance(node.op, ast.USub):
            operand = node.operand
            if isinstance(operand, ast.Constant):
                if isinstance(operand.value, (int, float)) and operand.value < 0:
                    mutated_node = copy.deepcopy(node)
                    mutated_node.operand.value = abs(operand.value)
                    yield mutated_node
            elif isinstance(operand, ast.Name):
                mutated_node = copy.deepcopy(node)
                mutated_node.op = ast.UAdd()
                yield mutated_node
class ReturnValuesMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
        if isinstance(node.value, ast.Call):
            func_name = node.value.func.attr  # Get the attribute name instead of the identifier
            if func_name == 'bool':
                mutated_node = copy.deepcopy(node)
                if isinstance(mutated_node.value.args[0], ast.NameConstant):
                    if mutated_node.value.args[0].value is True:
                        mutated_node.value.args[0] = ast.NameConstant(value=False)
                    elif mutated_node.value.args[0].value is False:
                        mutated_node.value.args[0] = ast.NameConstant(value=True)
                    yield mutated_node
            elif func_name in ['int', 'byte', 'short']:
                mutated_node = copy.deepcopy(node)
                if isinstance(mutated_node.value.args[0], ast.Num):
                    if mutated_node.value.args[0].n == 0:
                        mutated_node.value.args[0] = ast.Num(n=1)
                    else:
                        mutated_node.value.args[0] = ast.Num(n=0)
                    yield mutated_node
            elif func_name == 'long':
                mutated_node = copy.deepcopy(node)
                if isinstance(mutated_node.value.args[0], ast.Num):
                    mutated_node.value.args[0].n += 1
                    yield mutated_node
            elif func_name in ['float', 'double']:
                mutated_node = copy.deepcopy(node)
                if isinstance(mutated_node.value.args[0], ast.Num):
                    value = mutated_node.value.args[0].n
                    if not math.isnan(value):
                        mutated_node.value.args[0].n = -(value + 1.0)
                    else:
                        mutated_node.value.args[0].n = 0
                    yield mutated_node
            else:  # Object
                mutated_node = copy.deepcopy(node)
                mutated_node.value = ast.NameConstant(value=None)
                yield mutated_node
                if isinstance(mutated_node.value, ast.Call) and isinstance(mutated_node.value.args[0], ast.NameConstant) and mutated_node.value.args[0].value is None:

                    raise RuntimeError('Return value was null')

class VoidMethodCallMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Expr

    def mutate_node(self, node):
        if isinstance(node.value, ast.Call):
            func_name = node.value.func.attr  # Assumes function name is an identifier
            func_def = self.get_function_definition(node, func_name)
            if func_def is not None and isinstance(func_def.returns, ast.Name) and func_def.returns.id == 'None':
                mutated_node = ast.Pass()
                yield mutated_node

    def get_function_definition(self, node, func_name):
        while node:
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                return node
            node = node.parent
        return None
import ast

class PrimitiveReturnsMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
        if isinstance(node.value, (ast.Num, ast.NameConstant)):
            if isinstance(node.value, ast.Num):
                if isinstance(node.value.n, (int, float)):
                    mutated_node = ast.Return(value=ast.Num(n=0))
                    yield mutated_node
            elif isinstance(node.value, ast.NameConstant) and node.value.value in (True, False):
                mutated_node = ast.Return(value=ast.NameConstant(value=not node.value.value))
                yield mutated_node


class IncrementsMutator(MutationOperator):
    """
    The increments mutator will mutate increments, decrements, and assignment increments and decrements of local variables
    (stack variables). It will replace increments with decrements and vice versa.
    """

    def __init__(self):
        super().__init__()
        self.target_type = (ast.AugAssign,ast.Assign)
    
    def mutate_node(self, node):
        if isinstance(node, ast.AugAssign):
            if isinstance(node.op, ast.Add):
                # Replace increment (+=) with decrement (-=)
                mutated_node = copy.deepcopy(node)
                mutated_node.op = ast.Sub()
                yield mutated_node
            elif isinstance(node.op, ast.Sub):
                # Replace decrement (-=) with increment (+=)
                mutated_node = copy.deepcopy(node)
                mutated_node.op = ast.Add()
                yield mutated_node
        elif isinstance(node, ast.Assign):
            if isinstance(node.value, ast.BinOp):
                if isinstance(node.value.op, ast.Add):
                    # Replace assignment increment (x += y) with assignment decrement (x -= y)
                    mutated_node = copy.deepcopy(node)
                    mutated_node.value.op = ast.Sub()
                    yield mutated_node
                elif isinstance(node.value.op, ast.Sub):
                    # Replace assignment decrement (x -= y) with assignment increment (x += y)
                    mutated_node = copy.deepcopy(node)
                    mutated_node.value.op = ast.Add()
                    yield mutated_node


class EmptyReturnsMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
        if node.value is not None:
            mutated_node = copy.deepcopy(node)
            if isinstance(node.value, ast.Constant):
                if node.value.value == None:
                    mutated_node.value = ast.Constant(value=False)
                elif isinstance(node.value.value, bool):
                    mutated_node.value = ast.Constant(value=None)
                elif isinstance(node.value.value, int):
                    mutated_node.value = ast.Constant(value=0)
                elif isinstance(node.value.value, float):
                    mutated_node.value = ast.Constant(value=0.0)
                elif isinstance(node.value.value, str):
                    mutated_node.value = ast.Constant(value="")
                elif isinstance(node.value.value, bytes):
                    mutated_node.value = ast.Constant(value=b"")
                else:
                    mutated_node.value = ast.Constant(value=None)
            else:
                mutated_node.value = None
            yield mutated_node

class FalseReturnsMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
        if isinstance(node.value, ast.NameConstant) and node.value.value is True:
            mutated_node = copy.deepcopy(node)
            mutated_node.value = ast.NameConstant(value=False)
            yield mutated_node

class TrueReturnsMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
        if isinstance(node.value, ast.NameConstant) and node.value.value is False:
            mutated_node = copy.deepcopy(node)
            mutated_node.value = ast.NameConstant(value=True)
            yield mutated_node

def get_value_type(node):
    if isinstance(node, ast.NameConstant):
        return type(node.value).__name__
    elif isinstance(node, ast.Num):
        return type(node.n).__name__
    elif isinstance(node, ast.Str):
        return 'str'
    elif isinstance(node, ast.Bytes):
        return 'bytes'
    elif isinstance(node, ast.List):
        return 'list'
    elif isinstance(node, ast.Tuple):
        return 'tuple'
    elif isinstance(node, ast.Set):
        return 'set'
    elif isinstance(node, ast.Dict):
        return 'dict'
    elif isinstance(node, ast.Name):
        # assume it's a local variable
        return None
    else:
        # unknown node type
        return None

class NullReturnsMutator(MutationOperator):
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def has_not_null_annotation(self, node):
        """
        Checks whether a function has a @NotNull annotation.
        """
        func_def = None
        parent_node = node.parent
        while parent_node:
            if isinstance(parent_node, ast.FunctionDef):
                func_def = parent_node
                break
            parent_node = parent_node.parent
        if not func_def:
            return False
        for decorator in func_def.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == 'NotNull':
                return True
        return False

    def mutate_node(self, node):
        if not self.has_not_null_annotation(node):
            value_type = get_value_type(node)
            if value_type and value_type != 'None':
                mutated_node = copy.deepcopy(node)
                mutated_node.value = ast.NameConstant(value=None)
                yield mutated_node
