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


def open_shellcode(filename):

    shell2bin("shellcodes/" + filename, "badfile")
    exploit = mprotect.rop_exploit("badfile")
    os.remove("badfile")
    result.append((filename, len(exploit)))


def shellcodes():
    folder = os.getcwd() + "/shellcodes"
    for filename in os.listdir(folder):
        open_shellcode(filename)


shellcodes()
print(result)  # size in bytes
