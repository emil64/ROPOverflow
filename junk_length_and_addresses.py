# returns the junk data length, .data address and .bss address

from pygdbmi.gdbcontroller import GdbController
import re
import os


def get_addreses(gdb_response):
    _data = _bss = None
    for p in gdb_response:
        if p['payload'] is not None:
            if ".bss ALLOC" in p['payload']:
                _bss = int(re.findall(r'0x[0-9A-F]+', p['payload'], re.I)[0], 16)
            if ".data ALLOC" in p['payload']:
                _data = int(re.findall(r'0x[0-9A-F]+', p['payload'], re.I)[0], 16)
    return _data, _bss


def get_everything(exe):
    slack = -15
    signal = response = data_address = bss_address = None
    b = []

    while signal != 'SIGSEGV':

        slack += 15
        for x in range(1, 15):
            b.extend([x, x, x, x])

        f = open("file.bin", "wb")
        f.write(bytes(b))
        f.close()

        gdbmi = GdbController()
        gdbmi.write('file ' + exe)
        gdbmi.write('-break-insert main')
        gdbmi.write('-exec-arguments file.bin')
        gdbmi.write('-exec-run')
        response = gdbmi.write('maint info section')
        if data_address is None:
            (data_address, bss_address) = get_addreses(response)
        response = gdbmi.write('-exec-continue')
        # pprint(response)
        if response[-1]['payload']['reason'] == 'signal-received':
            signal = response[-1]['payload']['signal-name']

    address = response[-1]['payload']['frame']['addr']
    length = ((int(address[8:], 16) - 1) + slack) * 4

    if int(address[8:], 16) != int(address[2:4], 16):
        i = 10
        while int(address[i - 2:i], 16) != int(address[2:4], 16):
            length -= 1
            i -= 2
    os.remove("file.bin")
    return length, data_address, bss_address


def test():
    (padding, data, bss) = get_everything("vuln3-32-test")  # original binary from the lab
    # print(padding)
    # print(hex(data))
    # print(hex(bss))
    assert (padding == 44)
    assert (data == 0x80da060)
    assert (bss == 0x80db320)


test()
