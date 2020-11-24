# COMSM0051 Systems and Software Security Coursework
## Lab 4 Original Specifications
### Aim
Open a port on the victim machine using netcat tool that returns a shell (reverse shell exploit).
### Exploit Instructions
1. Download ROPGadget and install from [here](https://github.com/JonathanSalwan/ROPgadget)
1. Download official netcat release from [here](https://cs-uob.github.io/COMSM0049/code/nc071.tar.gz)
1. Extract and build netcat using `./configure` and `make`
1. Copy netcat to temporary folder using `cp src/netcat tmp/nc` (check using `/tmp/nc --help`)
1. Compile vuln3.c using `gcc -fno-stack-protector -m32 -static vuln3.c -o vuln3-32`
1. Build the exploit input string using `python lab4-exploit.py`. Provide an output file (e.g. `asd.bin`)
1. Run the compiled vulnerable binary passing the exploit file as input (e.g. `./vuln3-32 asd.bin`)
1. In a separate terminal run `$/tmp/nc 127.0.0.1 5678` and check if the reverse shell exploit is working
