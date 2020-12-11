#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[40];
	strcpy(buf, string);
	return (0);
}

void function15() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function14() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function13() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function12() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function11() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function10() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function9() {
	int count = 10;
	while (1) {
		count++;
	}	
}

void function8() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function7() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function6() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function5() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function4() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function3() {
	int count = 10;
	while (1) {
		count++;
	}
}

void function2(char* string) {
	while (1) {
		copyData(string);
	}
}

void function1(char* string) {
	while (1) {
		function2(string);
		function3();
		function4();
		function5();
		function6();
		function7();
		function8();
		function9();
		function10();
		function11();
		function12();
		function13();
		function14();
		function15();
	}
}

int main(int argc, char *argv[])
{
	char buffer[700];
	FILE *file;
    if (argc !=2)
    {
        printf("[*] invalid arguments!\n [*] > %s file_name\n",argv[0]);
        exit(0);
    }
	printf("opening file\n");
	file = fopen(argv[1],"rb");
	if (!file)
	{ 
		//printf("file not opened %s", strerror(errno));
		fprintf(stderr,"file not opened %s", strerror(errno));
		//printf("error");
		return (0);
	}
	printf("file opened\n");
	fread(buffer, 699,1,file);
	fclose(file);
	function1(buffer);
	return (0);
}
		

