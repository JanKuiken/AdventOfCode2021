
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


versions = []
def decode(depth=1):
    
    prefix = "  " * depth

    debug(prefix, bits[bits_pointer:])
    debug(prefix, "bits_pointer", bits_pointer)

    version = read_int(3)  
    type_id = read_int(3)

    debug(prefix, "version", version)
    debug(prefix, "type_id", type_id, ["operator", "values"][type_id==4])

    versions.append(version)

    if type_id == 4:

        value = read_literal_value()
        debug(prefix, "value", value)

    else: # other type id's are operators

        length_type_id = read_int(1)
        number_of_subpackets = 999999999999 # rediculious high
        length_of_subpackets = 999999999999 #      ,,
        if length_type_id == 1:
            number_of_subpackets = read_int(11)
        else: # length_type_id == 0
            length_of_subpackets = read_int(15)

        debug(prefix, "length_type_id", length_type_id, [15,11][length_type_id])
        debug(prefix, number_of_subpackets, length_of_subpackets)

        # oke, read sub packets
        packets_read = 0
        start_pointer = bits_pointer
        
        while (packets_read                   < number_of_subpackets and 
               (bits_pointer - start_pointer) < length_of_subpackets     ):
               
            # do stuff
            debug(prefix, "call decode (", bits_pointer, ", ",depth+1, ")")
            decode(depth+1)
            packets_read += 1
            
            debug(prefix, "read packets: ", packets_read)
            debug(prefix, "read bits: ", (bits_pointer - start_pointer))



if not test_mode:
    with open("input.txt") as f:
        line = f.readlines()[0].strip()
        bits = hex_str_to_bin_str(line)


print("=== part 1 ===")

if test_mode:
    #bits = hex_str_to_bin_str("D2FE28")
    #bits = hex_str_to_bin_str("38006F45291200")
    #bits = hex_str_to_bin_str("EE00D40C823060")
    #bits = hex_str_to_bin_str("8A004A801A8002F478")             # 16
    #bits = hex_str_to_bin_str("620080001611562C8802118E34")     # 12
    #bits = hex_str_to_bin_str("C0015000016115A2E0802F182340")   # 23
    bits = hex_str_to_bin_str("A0016C880162017C3686B18A3D4780") # 31

# note: bits and bits_pointer are global variables
bits_pointer = 0
print("len", len(bits))

decode()
print("\nversions", versions, sum(versions))

print("=== part 2 ===")




