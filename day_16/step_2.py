
# python script for AdventOfCode 2021, day 16, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

translate = {
    "0" : "0000",
    "1" : "0001",
    "2" : "0010",
    "3" : "0011",
    "4" : "0100",
    "5" : "0101",
    "6" : "0110",
    "7" : "0111",
    "8" : "1000",
    "9" : "1001",
    "A" : "1010",
    "B" : "1011",
    "C" : "1100",
    "D" : "1101",
    "E" : "1110",
    "F" : "1111",
}

# note: bits and bits_pointer are global variables
bits = ""
bits_pointer = 0

def hex_str_to_bin_str(s):
    bin_str = ""
    for c in s: bin_str += translate[c]
    return bin_str
    
def bin_str_to_int(s):
    return int(s, base=2)

def read_int(size):
    global bits, bits_pointer
    s = bits[bits_pointer : bits_pointer + size]
    bits_pointer += size
    return bin_str_to_int(s)

def read_bits(size):
    global bits, bits_pointer
    s = bits[bits_pointer : bits_pointer + size]
    bits_pointer += size
    return s

def read_literal_value():
    continue_reading = 1
    value = ""
    while continue_reading:
        continue_reading = read_int(1)
        v = read_bits(4)
        value += v
    return bin_str_to_int(value)

def debug(*args):
    if test_mode:
        print(*args)



def decode(node_to_be_filled, depth=1):
    
    prefix = "  " * depth

    version = read_int(3)  
    type_id = read_int(3)

    debug(prefix, "type_id", type_id, types[type_id])

    node_to_be_filled["type"] = type_id

    if type_id == 4:

        value = read_literal_value()
        debug(prefix, "value", value)
        
        node_to_be_filled["value"] = value
        

    else: # other type id's are operators

        length_type_id = read_int(1)
        number_of_subpackets = 999999999999 # rediculious high
        length_of_subpackets = 999999999999 #      ,,
        if length_type_id == 1:
            number_of_subpackets = read_int(11)
        else: # length_type_id == 0
            length_of_subpackets = read_int(15)

        # oke, read sub packets
        packets_read = 0
        start_pointer = bits_pointer
        
        while (packets_read                   < number_of_subpackets and 
               (bits_pointer - start_pointer) < length_of_subpackets     ):
            
            new_node = empty_node()
            node_to_be_filled["children"].append(new_node)
            # do stuff
            decode(new_node, depth+1)
            packets_read += 1

if not test_mode:
    with open("input.txt") as f:
        line = f.readlines()[0].strip()
        bits = hex_str_to_bin_str(line)

print("=== part 2 ===")

types = {
    0 : "sum",
    1 : "product",
    2 : "min",
    3 : "max",
    4 : "value",
    5 : "greater than",
    6 : "less than",
    7 : "equal",
}

def empty_node():
    return { "type": None, "value": None, "children" : [] }

def eval_node(node):
    
    child_values = [eval_node(child) for child in node["children"]]
    
    if node["type"] == 0:     # sum
        return sum(child_values)
    elif node["type"] == 1:   # product
        value = 1
        for v in child_values:
            value *= v
        return value
    elif node["type"] == 2:   # min
        return min(child_values)
    elif node["type"] == 3:   # max
        return max(child_values)
    elif node["type"] == 4:   # value
        return node["value"]
    elif node["type"] == 5:   # greater than
        return 1 if child_values[0] > child_values[1] else 0
    elif node["type"] == 6:   # less than
        return 1 if child_values[0] < child_values[1] else 0
    elif node["type"] == 7:   # equal
        return 1 if child_values[0] == child_values[1] else 0

if test_mode:
    #bits = hex_str_to_bin_str("C200B40A82") # 3
    #bits = hex_str_to_bin_str("04005AC33890") # 54
    #bits = hex_str_to_bin_str("880086C3E88112") # 7
    #bits = hex_str_to_bin_str("CE00C43D881120") # 9
    #bits = hex_str_to_bin_str("D8005AC2A8F0") # 1
    #bits = hex_str_to_bin_str("F600BC2D8F") # 0
    #bits = hex_str_to_bin_str("9C005AC2F8F0") # 0
    bits = hex_str_to_bin_str("9C0141080250320F1802104A08") # 1

bits_pointer = 0
start_node = empty_node()
decode(start_node)

print(eval_node(start_node))

