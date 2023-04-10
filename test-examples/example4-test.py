import sys

from example4 import add_numbers, subtract_numbers,multiply_numbers,divide_numbers,is_even,is_odd, compare_numbers, remove_unary_operator,replace_string,replace_variable,replace_integer,negate_boolean,invert_negatives

def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, 2) == 1
    assert add_numbers(0, 0) == 0

def test_subtract_numbers():
    assert subtract_numbers(1, 2) == -1
    assert subtract_numbers(-1, 2) == -3
    assert subtract_numbers(0, 0) == 0

def test_multiply_numbers():
    assert multiply_numbers(2, 3) == 6
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(0, 1) == 0

def test_divide_numbers():
    assert divide_numbers(6, 3) == 2
    assert divide_numbers(-6, 3) == -2
    assert divide_numbers(1, 2) == 0.5

def test_is_even():
    assert is_even(2) == True
    assert is_even(3) == False
    assert is_even(0) == True

def test_is_odd():
    assert is_odd(2) == False
    assert is_odd(3) == True
    assert is_odd(0) == False

def test_compare_numbers():
    assert compare_numbers(1, 1) == True
    assert compare_numbers(1, 2) == False
    assert compare_numbers(2, 1) == False

def test_negate_boolean():
    assert negate_boolean(True) == False
    assert negate_boolean(False) == True

def test_remove_unary_operator():
    assert remove_unary_operator(1) == -1
    assert remove_unary_operator(-1) == 1

def test_replace_integer():
    assert replace_integer(0) == 42
    assert replace_integer(10) == 52

def test_replace_string():
    assert replace_string("hello world") == "world world"
    assert replace_string("hello hello") == "world hello"

def test_replace_variable():
    assert replace_variable(0) == 1
    assert replace_variable(10) == 11

def test_invert_negatives():
    assert invert_negatives(1) == -1
    assert invert_negatives(-1) == 1
