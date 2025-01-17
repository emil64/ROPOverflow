
import address_pop
from address_pop import doubadd, pop_reg
import exploit_gadgets
from struct import pack
from address_pop import null_free

class Gadget():
    def __init__(self,name,gadget,dependencies=[]):
        self.name = name
        self.gadget = gadget
        self.dependencies = dependencies
        self.dcount = len(dependencies)
    
    def __str__(self):
        return self.name

class GadgetStore():
    def __init__(self,gadgets=[]):
        self.gadgets = gadgets
    
    def add(self,gadget):
        if type(gadget) == list:
            if gadget == []:
                pass
            else:
                self.gadgets.extend(gadget)
        else:
            self.gadgets.append(gadget)

    def search(self, name):
        return [x for x in self.gadgets if name in x.name]
    
    def __str__(self):
        return str([str(x) for x in self.gadgets])



def get_pop(rop,reg): 
    """Find a gadget that will pop a register
    
    :param rop: A instance of ROPgadgets
    :param reg: The register that will be popped
    :return: A list containing the packed 
    """
    # Attempt to find a pop reg ; ret gadget
    if rop.get_gadget(f"pop {reg} ; ret"):
        return Gadget(f"pop {reg}",pack('<I',rop.get_gadget(f"pop {reg} ; ret")))

    # Attempt to find a pop reg ; pop reg2 ; ret gadget
    for reg2 in ["eax", "ebx", "ecx", "edx"]:
        if rop.get_gadget(f"pop {reg} ; pop {reg2} ; ret"):
            return Gadget(f"pop {reg}", pack('<I',rop.get_gadget(f"pop {reg} ; pop {reg2} ; ret")),[f"{reg2}"])

    # Attempt to find pop that pops 3 gadgets
    for reg2 in ["eax", "ebx", "ecx", "edx"]:
        for reg3 in ["eax", "ebx", "ecx", "edx"]:
            if rop.get_gadget(f"pop {reg} ; pop {reg2} ; pop {reg3} ret"):
                return Gadget(f"pop {reg}", pack('<I',rop.get_gadget(f"pop {reg} ; pop {reg2} ; pop {reg3} ret")),[f"{reg2,reg3}"])

    print("NO GADGETS FOUND")
    return []

def get_zero_reg(rop,reg,gadgets):
    if rop.get_gadget(f"xor {reg}, {reg} ; ret"):
        return Gadget(f"zero {reg}", pack('<I',rop.get_gadget(f"xor {reg}, {reg} ; ret")))
        
    if rop.get_gadget(f"inc {reg} ; ret"):
        if len(gadgets.search(f"pop {reg}")) == 0:
            return []
        pop = gadgets.search(f"pop {reg}")[0]
        dependencies = pop.dependencies
        # Push ffffffff, increment register, and provide value for dependencies to eat
        return Gadget(f"zero {reg}",
                pop.gadget + pack('<I',0xffffffff) + (pack('<I',rop.get_gadget(f"inc {reg} ; ret")) * (len(dependencies) + 1)) , 
                dependencies)
    return []


# This should be refactored
def get_double_and_add(rop,reg):
    if rop.get_gadget(f"add {reg}, {reg} ; ret") and rop.get_gadget(f"inc {reg} ; ret"):
        return Gadget(f"DandA {reg}", pack("<I",rop.get_gadget(f"add {reg}, {reg} ; ret")) + pack("<I",rop.get_gadget(f"inc {reg} ; ret")))
    return []

def get_op_reg(rop, reg, op):
    gadgets = []
    if op in ["inc","dec"]:
        if rop.get_gadget(f"{op} {reg} ; ret"):
            return Gadget(f"{op} {reg}", pack("<I",rop.get_gadget(f"{op} {reg} ; ret")))
        else: 
            return []
    else:
        for reg2 in ["eax","ebx","ecx","edx"]:
            if reg2 != reg:
                if rop.get_gadget(f"{op} {reg}, {reg2} ; ret"):
                    gadgets.append(Gadget(f"{op} {reg}, {reg2}",
                                pack("<I",rop.get_gadget(f"add {reg}, {reg2} ; ret"))))
    return gadgets

def get_gadgets(rop):
    gadgets = GadgetStore()
    for reg in ["eax", "ebx", "ecx", "edx"]:
        gadgets.add(get_pop(rop,reg))
        gadgets.add(get_double_and_add(rop,reg))
        gadgets.add(get_zero_reg(rop,reg,gadgets))
        for op in ["add", "sub", "xor", "inc", "dec"]:
            gadgets.add(get_op_reg(rop,reg,op))
    return gadgets

def push_to_reg(address, reg, gadgets, rop):
    if null_free(address):
        pop_reg = gadgets.search(f"pop {reg}")[0]
        return [(pop_reg.gadget + pack("<I",address) * (pop_reg.dcount + 1) ,pop_reg.dependencies)]
    else:
        chains = []
        reg_gadgets = gadgets.search(f"{reg}")
        pop_reg =  gadgets.search(f"pop {reg}")

        if address == 0:
            zero = gadgets.search(f"zero {reg}")
            if zero != []:
                chains.append((zero[0].gadget,[]))

        if pop_reg != []:
            for gadget in reg_gadgets:
                for op in ["add","sub","xor"]:
                    if f"{op} {reg}" in gadget.name:
                        reg2 = gadget.name.split()[2]
                        pop_reg2 = gadgets.search(f"pop {reg2}")
                        if pop_reg2 != []:
                            chains.append(address_pop.pop_reg(address,pop_reg[0],pop_reg2[0],gadget,op))

                if f"inc {reg}" in gadget.name:
                    chain = address_pop.pop_reg(address,pop_reg[0],0,gadget,"inc")
                    if chain != -1:
                        chains.append(chain)
                if f"dec {reg}" in gadget.name:
                    chain = address_pop.pop_reg(address,pop_reg[0],0,gadget,"dec")
                    if chain != -1:
                        chains.append(chain)

        dabba =  GadgetStore(reg_gadgets).search(f"DandA")
        if dabba != []:
            zero = gadgets.search(f"zero {reg}")
            if zero != []:
                double = pack("<I",rop.get_gadget(f"add {reg}, {reg} ; ret"))
                add = pack("<I",rop.get_gadget(f"inc {reg} ; ret"))
                chains.append(address_pop.doubadd(address,zero[0],double,add))

        zero_reg = gadgets.search(f"zero {reg}")
        if zero_reg != []:
            inc = GadgetStore(reg_gadgets).search(f"inc {reg}")
            if inc != []:
                chain = address_pop.zero_and_inc(address,zero_reg[0],inc[0])
                if chain != -1:
                    chains.append(chain)

        if len(chains) != 0:
            return sorted(chains, key=lambda x: len(x[0]))
        
    print(f"Failed to push address {address} to reg {reg}")
    return -1



def main():
    binary_name = "vuln3-32-test"
    rop = exploit_gadgets.ROPgadgets(binary_name)
    print(get_gadgets(rop))

if __name__ == '__main__':
    main()
    