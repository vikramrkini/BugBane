from example1 import calculate_fibonacci, generate_primes

def test_calculate_fibonacci():
    assert calculate_fibonacci(0) == 0
    assert calculate_fibonacci(1) == 1
    assert calculate_fibonacci(2) == 1
    assert calculate_fibonacci(3) == 2
    assert calculate_fibonacci(4) == 3
    assert calculate_fibonacci(5) == 5
    assert calculate_fibonacci(6) == 8

def test_generate_primes():
    assert generate_primes(0) == []
    assert generate_primes(1) == []
    assert generate_primes(2) == [2]
    assert generate_primes(10) == [2, 3, 5, 7]
    assert generate_primes(20) == [2, 3, 5, 7, 11, 13, 17, 19]
