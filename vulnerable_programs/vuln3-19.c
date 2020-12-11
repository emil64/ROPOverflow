#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[2];
	strcpy(buf, string);
	return (0);
}

void function1(char* string);
void function2(char* string);
void function3();
void function4();
void function5(char* string);
void function6();
void function7(char* string);
void function8(char* string);
void function9();
void function10();

void function10() {
	int result = 10;
	for (int i = 0; i < 100; i++) {
		result++;
	}
}

void function9() {
	int result = 10;
	for (int i = 0; i < 100; i++) {
		result++;
	}
}

void function8(char* string) {
	int result = 10;
	copyData(string);
	while (result > 0) {
		result--;
	}
}

void function7(char* string) {
	int result = 0;
	function2(string);
	while (1) {
		result++;
	}
}

void function6() {
	for (int i = 0; i < 100; i++) {
		continue;
	}
}

void function5(char* string) {
	int count = 5;
	while (count > 0) {
		count--;
	}
	function8(string);
	for (int i = 0; i < 5; i++) {
		function9();
		function10();
	}
}

void function4() {
	while (1) {
		printf("function4\n");
	}
}

void function3() {
	while (1) {
		continue;
	}
}

void function2(char* string) {
	int result = 100;
	result *= 3;
	result += 25;
	if (result == 325) {
		function5(string);
		function6();
	} else {
		function7(string);
	}
}

void function1(char* string) {
	int result = 10;
	result = result * 2 + 1;
	if (result % 2) {
		function2(string);
	} else {
		function3();
		function4();
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
		

