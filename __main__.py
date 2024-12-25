import sys

from . import *

answers = {
    "p01_part1": 1646452,
    "p01_part2": 23609874,
    
    "p02_part1": 411,
    "p02_part2": 465,
    
    "p03_part1": 187194524,
    "p03_part2": 127092535,
    
    "p04_part1": 2462,
    "p04_part2": 1877,
    
    "p05_part1": 4959,
    "p05_part2": 4655,
    
    "p06_part1": 5239,
    "p06_part2": 1753,
    
    "p07_part1": 2314935962622,
    "p07_part2": 401477450831495,
    
    "p08_part1": 413,
    "p08_part2": 1417,
    
    "p09_part1": 6461289671426,
    "p09_part2": 6488291456470,
    
    "p10_part1": 496,
    "p10_part2": 1120,
    
    "p11_part1": 183435,
    "p11_part2": 218279375708592,
    
    "p12_part1": 1452678,
    "p12_part2": 873584,
    
    "p13_part1": 29187,
    "p13_part2": 99968222587852,
    
    "p14_part1": 216027840,
    "p14_part2": 6876,
    
    "p15_part1": 1294459,
    "p15_part2": 1319212,
    
    "p16_part1": 105508,
    "p16_part2": 548,
    
    "p17_part1": "1,3,5,1,7,2,5,1,6",
    "p17_part2": 236555997372013,
    
    "p18_part1": 356,
    "p18_part2": "22,33",
    
    "p19_part1": 360,
    "p19_part2": 577474410989846,
    
    "p20_part1": 1351,
    "p20_part2": 966130,
    
    "p21_part1": 197560,
    "p21_part2": 242337182910752,
    
    "p22_part1": 0,
    "p22_part2": 0,
    
    "p23_part1": 0,
    "p23_part2": 0,
    
    "p24_part1": 0,
    "p24_part2": 0,
    
    "p25_part1": 0,
    "p25_part2": 0,
}

def run_func(name):
    f = eval(name)
    actual = f()
    expected = answers[name]
    if actual == expected:
        msg = f"{actual} OK"
    else:
        msg = f"{actual} != {expected}"
    print(f"{name}: {msg}")

def main():
    args = sys.argv[1:]
    if len(args) > 0:
        # run the specified functions
        for name in args:
            run_func(name)
    else:
        module = dir(sys.modules[__name__])
        # run all functions
        for i in range(25):
            p = i + 1
            name1 = f"p{p:02}_part1"
            name2 = f"p{p:02}_part2"
            if name1 in module:
                run_func(name1)
            if name2 in module:
                run_func(name2)
        
if __name__ == '__main__':
    main()
