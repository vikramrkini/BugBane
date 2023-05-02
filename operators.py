import ast
import copy
import math

#### This file contains all the operators defined in Bugbane.

class MutationOperator:
    def __init__(self):
        self.target_type = None

    def mutate_node(self, node):
        raise NotImplementedError()
    
    def revert_node(self, node):
        raise NotImplementedError()
    
class ConditionalsBoundaryMutator(MutationOperator):
    """
    A mutation operator that replaces the relational operators <, <=, >, >= with their boundary counterpart.

    The original conditional is mutated to the following:
    - <  -> <=
    - <= -> <
    - >  -> >=
    - >= -> >

    Example:
    --------
    If the input node is "x < y", the mutated node will be "x <= y".
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.Compare

    def mutate_node(self, node):
        if isinstance(node, ast.Compare):
            mutated_node = copy.deepcopy(node)
            if isinstance(node.ops[0], ast.Lt):
                mutated_node.ops[0] = ast.LtE()
            elif isinstance(node.ops[0], ast.LtE):
                mutated_node.ops[0] = ast.Lt()
            elif isinstance(node.ops[0], ast.Gt):
                mutated_node.ops[0] = ast.GtE()
            elif isinstance(node.ops[0], ast.GtE):
                mutated_node.ops[0] = ast.Gt()
            yield mutated_node

    def revert_node(self, node):
        if isinstance(node, ast.Compare):
            reverted_node = copy.deepcopy(node)
            if isinstance(node.ops[0], ast.Lt):
                reverted_node.ops[0] = ast.GtE()
            elif isinstance(node.ops[0], ast.LtE):
                reverted_node.ops[0] = ast.Lt()
            elif isinstance(node.ops[0], ast.Gt):
                reverted_node.ops[0] = ast.LtE()
            elif isinstance(node.ops[0], ast.GtE):
                reverted_node.ops[0] = ast.Gt()
            return reverted_node


class IncrementsMutator(MutationOperator):
    """
    A mutation operator that replaces increments with decrements and vice versa.

    This mutator handles assignment increments and decrements (x+=1, x-=1).

    Example:
    --------
    If the input node is "x += 1", the mutated node will be "x -= 1".

    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.AugAssign

    def mutate_node(self, node):
        if isinstance(node, ast.AugAssign) and isinstance(node.op, (ast.Add, ast.Sub)):
            mutated_node = copy.deepcopy(node)
            if isinstance(node.op, ast.Add):
                mutated_node.op = ast.Sub()
            elif isinstance(node.op, ast.Sub):
                mutated_node.op = ast.Add()
            yield mutated_node

    def revert_node(self, node):
        if isinstance(node, ast.AugAssign) and isinstance(node.op, (ast.Add, ast.Sub)):
            reverted_node = copy.deepcopy(node)
            if isinstance(node.op, ast.Add):
                reverted_node.op = ast.Sub()
            elif isinstance(node.op, ast.Sub):
                reverted_node.op = ast.Add()
            return reverted_node
class InvertNegativesMutator(MutationOperator):
    """
    A mutation operator that inverts negation of integer and floating point variables.

    Example:
    --------
    If the input node is "-x", the mutated node will be "x".

    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.UnaryOp

    def mutate_node(self, node):
        """
        Inverts the negation of integer or float variables.

        Parameters:
        -----------
        node : ast.UnaryOp
            The UnaryOp node representing the negation operation.

        Returns:
        --------
        A generator that yields the mutated node.

        """
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            if isinstance(node.operand, (ast.Name, ast.Num)):
                mutated_node = copy.deepcopy(node)
                mutated_node.op = ast.UAdd()
                yield mutated_node

    def revert_node(self, node):
    
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            if isinstance(node.operand, (ast.Name, ast.Num)):
                reverted_node = copy.deepcopy(node)
                reverted_node.op = ast.USub()
                yield reverted_node

class MathMutator(MutationOperator):
    """
    A mutation operator that replaces binary arithmetic operations with another operation.

    Example:
    --------
    If the input node is "x + y", the mutated node will be "x - y".

    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.BinOp

    def mutate_node(self, node):
        if isinstance(node, ast.BinOp) :
            mutated_node = copy.deepcopy(node)
            if isinstance(node.op, ast.Add):
                mutated_node.op = ast.Sub()
            elif isinstance(node.op, ast.Sub):
                mutated_node.op = ast.Add()
            elif isinstance(node.op, ast.Mult):
                mutated_node.op = ast.Div()
            elif isinstance(node.op, ast.Div):
                mutated_node.op = ast.Mult()
            elif isinstance(node.op, ast.Mod):
                mutated_node.op = ast.Mult()
            elif isinstance(node.op, ast.BitAnd):
                mutated_node.op = ast.BitOr()
            elif isinstance(node.op, ast.BitOr):
                mutated_node.op = ast.BitAnd()
            elif isinstance(node.op, ast.BitXor):
                mutated_node.op = ast.BitAnd()
            elif isinstance(node.op, ast.LShift):
                mutated_node.op = ast.RShift()
            elif isinstance(node.op, ast.RShift):
                mutated_node.op = ast.LShift()
            elif isinstance(node.op, ast.FloorDiv):
                mutated_node.op = ast.Mult()
            yield mutated_node
    def revert_node(self, node):
    
        if isinstance(node.op, ast.Add):
            original_op = ast.Sub()
        elif isinstance(node.op, ast.Sub):
            original_op = ast.Add()
        elif isinstance(node.op, ast.Mult):
            original_op = ast.Div()
        elif isinstance(node.op, ast.Div):
            original_op = ast.Mult()
        elif isinstance(node.op, ast.Mod):
            original_op = ast.Mult()
        elif isinstance(node.op, ast.BitAnd):
            original_op = ast.BitOr()
        elif isinstance(node.op, ast.BitOr):
            original_op = ast.BitAnd()
        elif isinstance(node.op, ast.BitXor):
            original_op = ast.BitAnd()
        elif isinstance(node.op, ast.LShift):
            original_op = ast.RShift()
        elif isinstance(node.op, ast.RShift):
            original_op = ast.LShift()
        elif isinstance(node.op, ast.FloorDiv):
            original_op = ast.Mult()
        else:
            return  # Node not mutated by this operator

        original_node = copy.deepcopy(node)
        original_node.op = original_op
        yield original_node

class NegateConditionalsMutator(MutationOperator):
    """
    A mutation operator that negates conditionals.

    Example:
    --------
    If the input node is "x == y", the mutated node will be "x != y".

    """
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

    def revert_node(self, node, original_node):

        if isinstance(node, ast.Compare) and isinstance(original_node, ast.Compare):
            reverted_node = copy.deepcopy(original_node)
            if isinstance(original_node.ops[0], ast.Eq):
                reverted_node.ops[0] = ast.Eq()
            elif isinstance(original_node.ops[0], ast.NotEq):
                reverted_node.ops[0] = ast.NotEq()
            elif isinstance(original_node.ops[0], ast.LtE):
                reverted_node.ops[0] = ast.LtE()
            elif isinstance(original_node.ops[0], ast.GtE):
                reverted_node.ops[0] = ast.GtE()
            elif isinstance(original_node.ops[0], ast.Lt):
                reverted_node.ops[0] = ast.Lt()
            elif isinstance(original_node.ops[0], ast.Gt):
                reverted_node.ops[0] = ast.Gt()
            yield reverted_node


class VoidMethodCallMutator(MutationOperator):
    """
    A mutation operator that removes method calls to void methods.

    Example:
    --------
    If the input node is "someVoidMethod()", the mutated node will be "None".

    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.Call
        self.void_methods = set()

    def mutate_node(self, node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in self.void_methods:
            mutated_node = ast.NameConstant(value=None)
            yield mutated_node
    def revert_node(self, node):
    
        if node.value is None:
            original_node = copy.deepcopy(self.current_node)
            yield original_node


class FalseReturnsMutator(MutationOperator):
    """
    A mutation operator that replaces primitive and boxed boolean return values with false.

    Example:
    --------
    If the input node is "return True", the mutated node will be "return False".

    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
        if isinstance(node, ast.Return) and node.value:
            if isinstance(node.value, ast.NameConstant) and node.value.value is True:
                mutated_node = ast.NameConstant(value=False)
                yield ast.Return(value=mutated_node)
            elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id in ["bool", "int"]:
                mutated_node = ast.NameConstant(value=False)
                yield ast.Return(value=mutated_node)
            elif isinstance(node.value, ast.UnaryOp) and isinstance(node.value.op, ast.Not):
                if isinstance(node.value.operand, ast.NameConstant) and node.value.operand.value is False:
                    mutated_node = ast.NameConstant(value=True)
                    yield ast.Return(value=mutated_node)
                elif isinstance(node.value.operand, ast.Call) and isinstance(node.value.operand.func, ast.Name) and node.value.operand.func.id in ["bool", "int"]:
                    mutated_node = ast.NameConstant(value=True)
                    yield ast.Return(value=mutated_node)

    def revert_node(self, node):
        if isinstance(node, ast.Return) and node.value:
            if isinstance(node.value, ast.NameConstant) and node.value.value is False:
                mutated_node = ast.NameConstant(value=True)
                yield ast.Return(value=mutated_node)
            elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id in ["bool", "int"]:
                mutated_node = ast.NameConstant(value=True)
                yield ast.Return(value=mutated_node)
            elif isinstance(node.value, ast.UnaryOp) and isinstance(node.value.op, ast.Not):
                if isinstance(node.value.operand, ast.NameConstant) and node.value.operand.value is True:
                    mutated_node = ast.NameConstant(value=False)
                    yield ast.Return(value=mutated_node)
                elif isinstance(node.value.operand, ast.Call) and isinstance(node.value.operand.func, ast.Name) and node.value.operand.func.id in ["bool", "int"]:
                    mutated_node = ast.NameConstant(value=False)
                    yield ast.Return(value=mutated_node)

class TrueReturnsMutator(MutationOperator):
    """
    A mutation operator that replaces primitive and boxed boolean return values with true.

    Example:
    --------
    If the input node is "return False", the mutated node will be "return True".

    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
    
        if isinstance(node, ast.Return) and node.value is  None and isinstance(node.value, ast.NameConstant) and node.value.value is False:
            mutated_node = copy.deepcopy(node)
            mutated_node.value.value = True
            yield mutated_node

    def revert_node(self, node):
        if isinstance(node, ast.Return) and node.value is None and isinstance(node.value, ast.NameConstant) and node.value.value is True:
            reverted_node = copy.deepcopy(node)
            reverted_node.value.value = False
            return reverted_node


class NullReturnsMutator(MutationOperator):
    """Replaces return values with None.

    Methods that can be mutated by the EMPTY_RETURNS mutator or that are directly annotated with NotNull will not be mutated.

    """
    
    def __init__(self):
        super().__init__()
        self.target_type = ast.Return

    def mutate_node(self, node):
       
        if isinstance(node, ast.Return) and node.value is not None:
            mutated_node = copy.deepcopy(node)
            mutated_node.value = None
            yield mutated_node

    def revert_node(self, node, mutation):
        if isinstance(node, ast.Return) and node.value is None and mutation.target_type == ast.Return:
            return ast.Return(value=mutation.original_node.value)
        else:
            return node


class RemoveConditionalsMutator(MutationOperator):
    """
    The Remove Conditionals Mutator removes all conditional statements such that the guarded statements always execute.

    For example, if a block of code has an if statement that checks if a variable is equal to a constant:

    if some_variable == 5:
        # do something

    The mutator will remove the conditional, resulting in the following code:

    # do something

    This mutator can be useful for revealing code that is never executed, or for simplifying complex control flow.
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.If

    def mutate_node(self, node):
        if isinstance(node, ast.If):
            return node.body
        return None
    
    def revert_node(self,node, original_node):
        if isinstance(node, list):
            mutated_node = ast.If(
                test=original_node.test,
                body=node,
                orelse=original_node.orelse
            )
            return mutated_node
        return None
class Return(MutationOperator):
    target_type = ast.Return

    def __init__(self):
        self.old_value = None

    def mutate_node(self, node):
        self.old_value = node.value
        node.value = ast.Num(n=0)
        yield node

    def revert_node(self, node):
        node.value = self.old_value


class NotConditionMutator(MutationOperator):
    """
    A mutation operator that adds a 'not' in the if condition.

    Example:
    --------
    If the input node is "if x < y:", the mutated node will be "if not x < y:".
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.If

    def mutate_node(self, node):
        if isinstance(node, ast.If):
            # Convert "if not" to "if"
            if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
                mutated_node = copy.deepcopy(node)
                mutated_node.test = node.test.operand
                yield mutated_node
            # Add "not" to the if condition
            else:
                mutated_node = copy.deepcopy(node)
                mutated_node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
                yield mutated_node

    def revert_node(self, node):
        if isinstance(node, ast.If):
            # Revert "if not" to "if"
            if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
                reverted_node = copy.deepcopy(node)
                reverted_node.test = node.test.operand
                return reverted_node
            # Remove "not" from the if condition
            else:
                reverted_node = copy.deepcopy(node)
                reverted_node.test = node.test.operand
                return reverted_node

class BooleanInvertMutator(MutationOperator):
    """
    A mutation operator that changes True assignments to False and False assignments to True.

    Example:
    --------
    If the input node is "x = True;", the mutated node will be "x = False;".
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.Assign

    def mutate_node(self, node):
        if isinstance(node, ast.Assign):
            # Check if the assigned value is a boolean
            if isinstance(node.value, ast.NameConstant) and isinstance(node.value.value, bool):
                mutated_node = copy.deepcopy(node)
                mutated_node.value = ast.NameConstant(value=not mutated_node.value.value)
                yield mutated_node

    def revert_node(self, node):
        if isinstance(node, ast.Assign):
            # Check if the assigned value is a boolean
            if isinstance(node.value, ast.NameConstant) and isinstance(node.value.value, bool):
                reverted_node = copy.deepcopy(node)
                reverted_node.value = ast.NameConstant(value=not reverted_node.value.value)
                return reverted_node

class IfStatementSwapMutator(MutationOperator):
    """
    A mutation operator that swaps the order of the conditional branches in an if statement.

    Example:
    --------
    If the input node is "if x < y:\n    foo()\nelse:\n    bar()", the mutated node will be "if not x < y:\n    bar()\nelse:\n    foo()".
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.If
        pass

    def mutate_node(self, node):
        if isinstance(node, ast.If):
            mutated_node = copy.deepcopy(node)
            mutated_node.body, mutated_node.orelse = mutated_node.orelse, mutated_node.body
            mutated_node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
            yield mutated_node

    def revert_node(self, node):
        if isinstance(node, ast.If):
            reverted_node = copy.deepcopy(node)
            reverted_node.body, reverted_node.orelse = reverted_node.orelse, reverted_node.body
            reverted_node.test = reverted_node.test.operand
            return reverted_node
        

class FunctionCallArgumentSwapMutator(MutationOperator):
    """
    A mutation operator that swaps the order of arguments in a function call.

    Example:
    --------
    If the input node is "foo(x, y)", the mutated node will be "foo(y, x)".
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.Call
        

    def mutate_node(self, node):
        if isinstance(node, ast.Call):
            for i in range(len(node.args)):
                mutated_args = copy.deepcopy(node.args)
                mutated_args[i], mutated_args[(i+1)%len(mutated_args)] = mutated_args[(i+1)%len(mutated_args)], mutated_args[i]
                mutated_node = copy.deepcopy(node)
                mutated_node.args = mutated_args
                yield mutated_node

    def revert_node(self, node):
        return copy.deepcopy(node)

class StatementDeletionMutator(MutationOperator):
    """
    A mutation operator that deletes a statement from the code.

    Example:
    --------
    If the input node is "x = y + 2;\nfoo(x);", the mutated node will be "foo(x);".
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.stmt
               

    def mutate_node(self, node):
        if isinstance(node, ast.stmt):
            mutated_node = None
            if hasattr(node, "parent"):
                mutated_node = copy.deepcopy(node.parent)
                for i, child in enumerate(mutated_node.body):
                    if child == node:
                        mutated_node.body.pop(i)
                        break
            yield mutated_node

    def revert_node(self, node):
        return copy.deepcopy(node)
    
class BooleanOperatorMutator(MutationOperator):
    """
    A mutation operator that replaces boolean operators with their counterparts.

    Example:
    --------
    If the input node is "x and y", the mutated node will be "x or y".
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.BoolOp

    def mutate_node(self, node):
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
            mutated_node = copy.deepcopy(node)
            mutated_node.op = ast.Or()
            yield mutated_node
        elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
            mutated_node = copy.deepcopy(node)
            mutated_node.op = ast.And()
            yield mutated_node

    def revert_node(self, node):
        return copy.deepcopy(node)
    
class BitwiseOperatorMutator(MutationOperator):
    """
    A mutation operator that mutates bitwise and (&) and or (|) by swapping them.
    """
    def __init__(self):
        super().__init__()
        self.target_type = ast.BinOp

    def mutate_node(self, node):
        if isinstance(node.op, (ast.BitAnd, ast.BitOr, ast.BitXor)):
            # Swap the operators
            swapped_node = copy.deepcopy(node)
            if isinstance(node.op, ast.BitAnd):
                swapped_node.op = ast.BitOr()
            elif isinstance(node.op, ast.BitOr):
                swapped_node.op = ast.BitXor()
            elif isinstance(node.op, ast.BitXor):
                swapped_node.op = ast.BitAnd()
            yield swapped_node

    def revert_node(self, node):
        reverted_node = copy.deepcopy(node)
        if isinstance(node.op, ast.BitAnd):
            reverted_node.op = ast.BitXor()
        elif isinstance(node.op, ast.BitOr):
            reverted_node.op = ast.BitAnd()
        elif isinstance(node.op, ast.BitXor):
            reverted_node.op = ast.BitOr()
        return reverted_node
