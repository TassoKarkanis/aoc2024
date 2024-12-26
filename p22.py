from .utils import *

Base19 = ["A", "B", "C", "D", "E",
          "F", "G", "H", "I", "J",
          "K", "L", "M", "N", "O",
          "P", "Q", "R", "S"]

def base19(x):
    # Returns the 4-digit base 19 representation of a string
    a = Base19[x % 19]
    
    x //= 19
    b = Base19[x % 19]
    
    x //= 19
    c = Base19[x % 19]
    
    x //= 19
    d = Base19[x % 19]

    return d + c + b + a

def test_base19():
    data = ((0, "AAAA"),
            (1, "AAAB"),
            (2, "AAAC"),
            (18, "AAAS"),
            (19, "AABA"),
            )

    for d in data:
        # print(f"{d[0]}  exp({d[1]}) act({base19(d[0])})")
        assert base19(d[0]) == d[1]

def predict1(x):
    # multiply by 64, mix, and prune
    x ^= 64*x
    x %= 16777216

    # divide by 32, mix, and prune
    x ^= x // 32
    x %= 16777216

    # multiply by 2048, mix, and prune
    x ^= 2048*x
    x %= 16777216
    return x

def predict(x, n):
    for _ in range(n):
        x = predict1(x)
    return x

def test_predict():
    assert predict(123,1) == 15887950
    assert predict(123,2) == 16495136
    assert predict(123,3) == 527345
    assert predict(123,4) == 704524
    assert predict(123,5) == 1553684
    assert predict(123,6) == 12683156
    assert predict(123,7) == 11100544
    assert predict(123,8) == 12249484
    assert predict(123,9) == 7753432
    assert predict(123,10) == 5908254

    assert predict(1, 2000) == 8685429
    assert predict(10, 2000) == 4700978
    assert predict(100, 2000) == 15273692
    assert predict(2024, 2000) == 8667524

def p22_part1():
    # run the tests
    test_base19()
    test_predict()

    # compute the solution
    with open(get_data_file("p22-data.txt")) as fp:
        data = fp.read()
    total = 0
    for x in data.splitlines():
        x = int(x)
        total += predict(x, 2000)
    return total

def get_prices(x):
    # form the secret keys
    s = [x]
    for i in range(2000):
        s.append(predict1(s[i]))

    # get the prices
    prices = [s[i] % 10 for i in range(2001)]
    return prices

def get_delta_string(prices):
    # get the deltas
    deltas = [prices[i+1] - prices[i] for i in range(2000)]

    # get delta string
    s = [Base19[d + 9] for d in deltas]
    return "".join(s)

Data1 = """1
2
3
2024"""

def get_data(data):
    lines = data.splitlines()
    return list(map(int, lines))

# Algorithm:
#
# 1) Compute all the 2000 secret keys.
#
# 2) Compute the deltas, and encode them in base 19 strings so each
#    delta is one character.
#
# 3) Count to 4^19 in base 19, generate the corresponding string,
#    search in each delta string.
#
# 4) Aggregate "price" in each string.  Find maximum.

def solve(keys):
    # get the price data and delta encodings
    all_prices = [get_prices(x) for x in keys]

    # get all the delta strings
    all_strings = [get_delta_string(p) for p in all_prices]

    # find the maximum 
    N = 19**4
    max_total = 0
    for i in range(N):
        # print(f"{i}/{N}")
        
        total = 0
        pattern = base19(i)
        for prices, s in zip(all_prices, all_strings):
            j = s.find(pattern)
            if j >= 0:
                total += prices[j+4]

        if total > max_total:
            max_total = total

    return max_total

# Algorithm:  Like solve(), but do 19 sequences "at once".

def solve2(keys):
    # get the price data and delta encodings
    all_prices = [get_prices(x) for x in keys]

    # get all the delta strings
    all_strings = [get_delta_string(p) for p in all_prices]

    # 3-digit partial pattern
    # Power = 3
    # ScaleK = 19
    # PartialEnd = 3
    # MaxIndex = 1997
    # FullPatternOffset = 3

    # 2-digit partial pattern
    Power = 2
    ScaleK = 19*19
    PartialEnd = 2
    MaxIndex = 1997
    FullPatternOffset = 2

    # find the maximum
    N = 19**Power
    max_total = 0
    for k in range(N):
        # print(f"{k}/{N}")
        
        # make a pattern with 3 digits
        partial_pattern = base19(k*ScaleK)[0:PartialEnd]

        # maps (pattern,i) -> bool
        price_map = {}

        # maps pattern -> price
        results = {}

        # search for this pattern
        for i in range(len(all_strings)):
            s = all_strings[i]

            # search repeatedly
            index = 0
            while True:
                j = s.find(partial_pattern, index)
                if j < 0 or j >= MaxIndex:
                    break
                
                # check/record this result
                pattern = partial_pattern + s[j+FullPatternOffset:j+4]
                key = (pattern,i)
                if key not in price_map:
                    # update the price map
                    price_map[key] = True

                    # also update the results map
                    price = all_prices[i][j+4]
                    if pattern not in results:
                        results[pattern] = price
                    else:
                        results[pattern] += price

                # update the index
                index = j+1

        # process the results
        for _, price in results.items():
            if price > max_total:
                max_total = price

    return max_total

def p22_part2():
    # run the tests
    test_base19()
    test_predict()

    # total = solve2(get_data(Data1))
    # print(f"total: {total}")
    # assert total == 23

    # compute the solution
    with open(get_data_file("p22-data.txt")) as fp:
        data = fp.read()
    total = solve2(get_data(data))
    return total

__all__ = ["p22_part1", "p22_part2"]
