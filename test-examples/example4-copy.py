def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide_numbers(a, b):
    return a / b

def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return n % 2 != 0

def compare_numbers(a, b):
    if a == b:
        return True
    else:
        return False

def negate_boolean(boolean_value):
    return not boolean_value

def remove_unary_operator(value):
    return -value

def replace_integer(value):
    return value + 42

def replace_string(value):
    return value.replace('hello', 'world')

def replace_variable(x):
    y = x + 1
    return y

def invert_negatives(value):
    return -value