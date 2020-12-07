import sys
import os
import re
import binascii
import time

sys.path.append('../')
import ropoverflow

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
        if ".bin" in filename:
            exploit = ropoverflow.rop_exploit(binary_name)
        else:
            shell2bin("shellcodes/" + filename, "badfile")
            exploit = ropoverflow.rop_exploit(binary_name)
            os.remove("badfile")
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
    print(f'Average CPU time is: {average}')


def test():
    shellcodes("vuln3-32-test")
    print(result)  # size in bytes
    #lines of code: pygount - -format = summary - -folders - to - skip = "[eval, netperf-netperf-2.6.0, __pycache__, venv, vulnerable_binaries, .git, .idea, .vagrant]"

if __name__ == "__main__":
    test()
