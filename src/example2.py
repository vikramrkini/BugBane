def multiply(a, b):
    result = a * b
    return result

def divide(a, b):
    if b == 0:
        return None
    result = a / b
    return result

def negate_boolean(value):
    return not value

def remove_unary_operator(value):
    return -value

def replace_integer(value):
    return value + 1


def complex_function(a, b):
    if a < 0:
        return b
    elif a > 100:
        return None
    else:
        result = (a + b) * 2
        return result