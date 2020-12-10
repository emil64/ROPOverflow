import sys
import os
import re
import binascii
import time
from functools import reduce

sys.path.append('../')
import ropoverflow
import input_length
import exploit_gadgets

result = []


def shell2bin(shellcode, binary):
    with open(shellcode, "r") as fileshell:
        flux = fileshell.read()
        flux = re.sub("[^0-9,^a-fA-F]", "", flux)
        fileshell.close()
    with open(binary, "wb") as filebin:
        filebin.write(binascii.unhexlify(flux))
        filebin.close()


def open_shellcode(binary_name, filename):
    if ".exclude" not in filename:
        print("Testing " + filename)
        (padding, _, bss) = input_length.get_everything(binary_name)
        if ".hex" in filename:
            shell2bin("shellcodes/" + filename, "badfile")
            exploit = ropoverflow.rop_exploit(binary_name, padding, bss)
            os.remove("badfile")
        else:
            exploit = ropoverflow.rop_exploit(binary_name, padding, bss)
        result.append((filename, len(exploit)))


def get_time(start):
    elapsed_time = (time.time() - start)
    return elapsed_time


def shellcodes(binary_name):
    average = 0.0
    folder = os.getcwd() + "/shellcodes"
    for filename in os.listdir(folder):
        start = time.time()
        open_shellcode(binary_name, filename)
        average += get_time(start)
    average = average / len(os.listdir(folder))
    return average


def padding_time(binary):
    average = 0.0
    for i in range(1, 10):
        start = time.time()
        input_length.get_everything(binary)
        average += get_time(start)
    average = average / 10
    return average


def gadgets_time(binary):
    average = 0.0
    for i in range(1, 10):
        start = time.time()
        exploit_gadgets.ROPgadgets(binary)
        average += get_time(start)
    average = average / 10
    return average


def gadgets_usage_per_bin(binary):
    rop = exploit_gadgets.ROPgadgets(binary)
    total = len(rop.get_gadgets())
    exploit = ropoverflow.rop_exploit(binary, 0, 0xffffffff)
    if exploit == -1:
        return binary, total, -1
    uniques = reduce(lambda x, y: ((y in x) and x) or x + [y], exploit, [])
    gadgets_used = len(uniques)
    return total, gadgets_used


def gadgets_usage():
    folder = os.getcwd() + "/binaries/"
    usage = []
    for filename in os.listdir(folder):
        t, gu = gadgets_usage_per_bin(folder + filename)
        usage.append((filename, t, gu))
    return usage


def test():
    test_binary = "vuln3-32-test"
    average = shellcodes(test_binary)  # size in bytes
    p_time = padding_time(test_binary)
    g_time = gadgets_time(test_binary)
    g_usage = gadgets_usage()
    print("\n\n\n")
    print(f"Payload sizes: {result}")
    print(f"Average CPU timpe: {average}")
    print(f"Avergage time to find padding: {p_time}")
    print(f"Avergage time to find gadgets: {g_time}")
    print(f"Gadgets usage: {g_usage}")
    # lines of code: pygount --format=summary --folders-to-skip="[eval,netperf-netperf-2.6.0,__pycache__,
    # venv,vulnerable_binaries,.git,.idea,.vagrant]"


if __name__ == "__main__":
    test()
