import re

from .utils import *

def match_char(data, c):
    if len(data) < 1 or data[0] != c:
        return False, data

    data = data[1:]
    return True, data

def match_3digits(data):
    m = re.search("^[0-9]+", data)
    if not m:
        return None, data

    digits = m.group(0)
    if len(digits) > 3:
        return None, data

    # remove the digits and return
    data = data[len(digits):]
    return digits, data

def match_substr(data, substr):
    try:
        i = data.index(substr)
    except:
        return None, data

    # remove the prefix
    data = data[i + len(substr):]
    return i, data

def compute_product(data, part2):
    # literals instructions
    mul_str = "mul("
    do_str = "do()"
    dont_str = "don't()"

    product = 0
    enabled = True
    while True:
        # find next occurrence of "mul("
        mul, mul_data = match_substr(data, mul_str)
        if mul is None:
            break

        # find the next occurrence of do/don't
        if enabled:
            e_str = dont_str
        else:
            e_str = do_str
        e, e_data = match_substr(data, e_str)

        # check which comes first
        if part2 and e is not None and e < mul:
            enabled = not enabled
            data = e_data
            continue
        else:
            data = mul_data

        # match the first number
        d1, data = match_3digits(data)
        if d1 is None:
            continue
        
        # match the comma
        ok, data = match_char(data, ',')
        if not ok:
            continue

        # match the second number
        d2, data = match_3digits(data)
        if d2 is None:
            continue

        # match the closing paren
        ok, data = match_char(data, ')')
        if not ok:
            continue

        # accumulate the product
        if enabled:
            product += int(d1)*int(d2)

    return product

Data1 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def get_data():
    with open(get_data_file("p03-data.txt")) as fp:
        data = fp.read()
    return data

def p03_part1():
    # run the tests
    assert compute_product(Data1, False) == 161

    # compute the solution
    data = get_data()
    return compute_product(data, False)

def p03_part2():
    # run the tests
    assert compute_product(Data1, True) == 48

    # compute the solution
    data = get_data()
    return compute_product(data, True)


__all__ = ["p03_part1", "p03_part2"]
