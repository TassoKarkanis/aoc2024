from .utils import *

Data1 = "2333133121414131402"

def get_test_data():
    return Data1

def get_full_data():
    with open(get_data_file("p09-data.txt")) as fp:
        data = fp.read().strip()
    return data
    
def block_string(blocks):
    return "".join([str(b) for b in blocks])

def decode_disk_map(disk_map):
    blocks = []
    file_id = 0
    while len(disk_map) != 0:
        # get the file length
        file_len = int(disk_map[0])
        disk_map = disk_map[1:]

        # get the empty length
        empty_len = 0
        if len(disk_map) > 0:
            empty_len = int(disk_map[0])
            disk_map = disk_map[1:]

        # add the file blocks
        blocks.extend([file_id]*file_len)

        # add the empty space
        blocks.extend(["."]*empty_len)

        # increment the file ID
        file_id += 1
    return blocks

def compactify(blocks):
    i = 0
    j = len(blocks) - 1

    def advance_i():
        nonlocal i
        while blocks[i] != "." and i < len(blocks):
            i += 1

    def retreat_j():
        nonlocal j
        while blocks[j] == "." and j > 0:
            j -= 1
    
    while True:
        # update the pointers
        advance_i()
        retreat_j()

        # check for termination condition
        if i >= j:
            break

        # swap the blocks
        tmp = blocks[i]
        blocks[i] = blocks[j]
        blocks[j] = tmp
    
def checksum(blocks):
    s = 0
    for i, file_id in enumerate(blocks):
        # ignore empty blocks
        if file_id == ".":
            continue
        
        s += i*file_id
    return s

def part1(disk_map):
    blocks = decode_disk_map(disk_map)
    compactify(blocks)
    return checksum(blocks)

def p09_part1():
    # run the tests
    data = get_test_data()
    assert part1(data) == 1928

    # compute the solution
    data = get_full_data()
    return part1(data)
    
    
def decode_disk_map2(disk_map):
    file_list = []
    offset = 0
    file_id = 0
    while len(disk_map) != 0:
        # get the file length
        file_len = int(disk_map[0])
        disk_map = disk_map[1:]

        # get the empty length
        empty_len = 0
        if len(disk_map) > 0:
            empty_len = int(disk_map[0])
            disk_map = disk_map[1:]

        # entry the entry to file list
        entry = (file_id, offset, file_len)
        file_list.append(entry)

        # update the offset
        offset += file_len + empty_len
        
        # increment the file ID
        file_id += 1
    return file_list

def file_list_string(file_list):
    last_offset = 0
    string = ""
    for e in file_list:
        # add empty space if necessary
        delta = e[1] - last_offset
        if delta > 0:
            string += "." * delta

        # add the string for this file
        string += str(e[0]) * e[2]

        # update the last offset
        last_offset = e[1] + e[2]
    return string

def compactify2(file_list):
    # get the file ID's
    file_ids = [e[0] for e in file_list]

    # visit the file ID's in reverse order
    # print(file_list)
    for file_id in reversed(file_ids):
        # get the index of this file ID
        index = [i for i, e in enumerate(file_list) if e[0] == file_id][0]
        entry = file_list[index]

        # move it up, if possible
        for i0 in range(index):
            i1 = i0 + 1

            # get the entries
            e0 = file_list[i0]
            e1 = file_list[i1]

            # get the offsets describing the empty space between
            off0 = e0[1] + e0[2]
            off1 = e1[1]

            # check if it fits here
            if off1 - off0 >= entry[2]:
                # remove it from it's current location
                file_list[index:index+1] = []

                # update it
                entry = (entry[0], off0, entry[2])

                # insert it
                file_list[i1:i1] = [entry]
                break

        # print(file_list)
        # print(file_list_string(file_list))

def file_list_checksum(file_list):
    s = 0
    for e in file_list:
        for off in range(e[1],e[1]+e[2]):
            s += int(e[0])*off
    return s

def part2(disk_map):
    file_list = decode_disk_map2(disk_map)
    compactify2(file_list)
    return file_list_checksum(file_list)

def p09_part2():
    # run the tests
    data = get_test_data()
    assert part2(data) == 2858

    # compute the solution
    data = get_full_data()
    return part2(data)
    
__all__ = ["p09_part1", "p09_part2"]
