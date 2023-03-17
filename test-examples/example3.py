def find_largest(numbers):
    largest = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] >= largest:  # mutation introduced here
            largest = numbers[i]
    return largest
