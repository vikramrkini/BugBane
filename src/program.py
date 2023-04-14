def check_numbers(a, b, c):
    if a > b and a > c:
        return f"{a} is the largest number."
    elif b > a and b > c:
        return f"{b} is the largest number."
    elif c > a and c > b:
        return f"{c} is the largest number."
    elif a == b == c:
        return "All numbers are equal."
    else:
        return "None of the numbers is the largest."
