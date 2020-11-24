# Remove null bytes from address
from struct import pack



def push_reg(address,pop_reg, pop_reg2, a_gadget):
    """Creates a packed struct which pops the address into the struct, using the 
    arithmetic gadget if required
    
    :param address: The address that may contain a null byte
    :param pop_reg: Address of a gadget that pops the stack into a register
    :param pop_reg2: Address of a gadget that pops the stack into a second register
    :param a_gadget: Address of an arithmetic gadget that stores the result of 
        some arithmetic operation of reg and reg2 (currently only supporting add)
        which stores the result in reg
    :return: A packed struct that pushes address into pop_reg
    """
    if null_free(address):
            return pack("<I",address) + pack("<I",pop_reg)
    else:
        mask, masked_address = get_mask_add(address)
        return pack("<I",mask) + pack("<I", masked_address)\
            + pack("<I", pop_reg) + pack("<I", pop_reg2) + pack("<I",a_gadget)


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
    