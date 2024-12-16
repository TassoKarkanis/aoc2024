from .utils import *

Rules = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13"""

Updates = """75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def is_correct(u, rules):
    # determine if the update is correct
    correct = True
    for r in rules:
        # find the indices, if available
        try:
            i0 = u.index(r[0])
            i1 = u.index(r[1])
        except:
            continue

        if i0 > i1:
            correct = False
            break
    return correct

def get_data(rules_raw, updates_raw):
    rules = rules_raw.splitlines()
    updates = updates_raw.splitlines()

    # make the rules pairs
    rules = [list(r.split("|")) for r in rules]

    # make the updates lists
    updates = [list(u.split(",")) for u in updates]
    
    return rules, updates

def get_test_data():
    return get_data(Rules, Updates)

def get_all_data():
    with open(get_data_file("p05-rules.txt")) as fp:
        rules = fp.read()
    with open(get_data_file("p05-updates.txt")) as fp:
        updates = fp.read()

    return get_data(rules, updates)

def compute_part1(rules, updates):
    count = 0

    # iterate over the updates
    for u in updates:
        correct = is_correct(u, rules)
        
        # if the update is correct, get the middle page number
        if correct:
            p = u[len(u)//2]
            count += int(p)

    return count

def p05_part1():
    # run the tests
    rules, updates = get_test_data()
    assert compute_part1(rules,updates) == 143

    # compute the solution
    rules, updates = get_all_data()
    return compute_part1(rules, updates)

def compute_part2(rules, updates):
    count = 0

    # iterate over the updates
    for u in updates:
        if is_correct(u, rules):
            continue

        # swap pages until all rules are satisfied
        while True:
            modified = False
            for r in rules:
                # find the indices, if available
                try:
                    i0 = u.index(r[0])
                    i1 = u.index(r[1])
                except:
                    continue
            
                # if the rule is not satisfied, swap the pages
                if i0 > i1:
                    modified = True
                    tmp = u[i0]
                    u[i0] = u[i1]
                    u[i1] = tmp

            if not modified:
                break

        # update the count
        p = u[len(u)//2]
        count += int(p)

    return count

def p05_part2():
    # run the tests
    rules, updates = get_test_data()
    assert compute_part2(rules,updates) == 123

    # compute the solution
    rules, updates = get_all_data()
    return compute_part2(rules, updates)
    
__all__ = ["p05_part1", "p05_part2"]
