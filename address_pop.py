# Remove null bytes from address
from ctypes import addressof
from logging import log
from struct import pack



def pop_reg(address,reg, reg2, a_gadget,mode):
    """Creates a packed struct which pops the address into the struct, using the 
    arithmetic gadget if required
    
    :param address: The address that may contain a null byte
    :param reg: Gadget that pops the stack into a register
    :param reg2: Gadget that pops the stack into a second register
    :param a_gadget: Arithmetic gadget that stores the result of 
        some arithmetic operation of reg and reg2 (currently only supporting add)
        which stores the result in reg
    :param mode: The type of agadget, member of [add,sub,xor,inc,dec]
    :return: A packed struct that pops address into reg
    """
    if null_free(address):
            return  reg + pack("<I",address)
    else:
        print(f"Modified {address:x} using {mode}")
        if mode in ["add","sub","xor"]:
            mask, masked_address = 0, 0
            if mode == "add":
                mask, masked_address = get_mask_add(address)
            elif mode == "sub":
                mask, masked_address = get_mask_sub(address)
            elif mode == "xor":
                mask, masked_address = get_mask_xor(address)
            return reg + pack("<I",masked_address) + reg2 +  pack("<I", mask) + a_gadget
        elif mode in ["inc","dec"]:
            a_chain = b""
            if mode == "inc":
                while not null_free(address):
                    address -= 1
                    a_chain += a_gadget
            elif mode == "dec":
                while not null_free(address):
                    address += 1
                    a_chain += a_gadget
            print(address)
            return reg + pack('<I', address) + a_chain


def null_free(address):
    for i in range(4):
        if ((address >> (8 * i)) % 256) == 0:
            return False
    return True

def get_mask_add(address):
    for mask in range(0x01010101,0xffffffff):
        if null_free(mask):
            if null_free((address-mask)):
                return mask, (address-mask)%(1<<32)

def get_mask_sub(address):
    for mask in range(0x01010101,0xffffffff):
        if null_free(mask):
            if null_free((address+mask)):
                return mask, (address+mask)%(1<<32)

def get_mask_xor(address):
    mask = 0
    for i in range(4):
        for mask_byte in range(1,256):
            if ((address >> (8 * i)) % 256) ^ mask_byte != 0:
                mask += mask_byte << (8*i)
                break
    return mask, (address^mask)


def doubadd(address,double,add):
    out = b""
    for i in range(31,0,-1):
        if (address >> i) & 0x1 == 1:
           out += add + double 
        else:
           out += double
    if (address & 0x1):
        out += add
    return out







def test():
    assert(null_free(0x12345678))
    assert(not null_free(0x00123456))

    for inp in [0x00123456,0x01000000,0x00FFFFFF,0x00011101]:
        print(f"Masking {inp:8x}:")
        out = get_mask_add(inp)
        print(f"{out[1]:8x} + {out[0]:8x} = {(out[1]+out[0])%(1<<32):8x}")
        out = get_mask_sub(inp)
        print(f"{out[1]:8x} - {out[0]:8x} = {(out[1]-out[0])%(1<<32):8x}")
        out = get_mask_xor(inp)
        print(f"{out[1]:8x} ^ {out[0]:8x} = {(out[1]^out[0]):8x}")




if __name__ == '__main__':
    test()
    