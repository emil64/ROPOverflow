import sys
import os
import re
import binascii

sys.path.append('../')
import mprotect

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

    shell2bin("shellcodes/" + filename, "badfile")
    exploit = mprotect.rop_exploit(binary_name, "badfile")
    os.remove("badfile")
    result.append((filename, len(exploit)))


def shellcodes(binary_name):
    folder = os.getcwd() + "/shellcodes"
    for filename in os.listdir(folder):
        open_shellcode(binary_name, filename)


def test():
    shellcodes("vuln3-32-test")
    print(result)  # size in bytes


if __name__ == "__main__":
    test()
