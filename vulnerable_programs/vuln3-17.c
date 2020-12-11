#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[5];
	strcpy(buf, string);
	return (0);
}

void function11(int result, char* string) {
	while (1) {
		function11(result, string);
	}
}

void function10(int result, char* string) {
	while (1) {
		result--;
	}
}

void function9(int result, char* string) {
	for (int i = 0; i < 100; i++) {
		result++;
		function11(result, string);
	}
}

void function8(int result, char* string) {
	result += result;
	copyData(string);
}

void function7(int result, char* string) {
	while (1) {
		result++;
	}
}

void function6(int result, char* string) {
	while (1) {
		result--;
	}
}

void function5(int result, char* string) {
	result -= result;
	if (result == 0) {
		function10(result, string);
	} else {
		function11(result, string);
	}
}

void function4(int result, char* string) {
	result += result;
	if (result >= 10000) {
		function8(result, string);
	} else {
		function9(result, string);
	}
}

void function3(int result, char* string) {
	result /= result;
	if (result == 1) {
		function6(result, string);
	} else {
		function7(result, string);
	}
}

void function2(int result, char* string) {
	result *= result;
	if (result % 2 == 0) {
		function4(result, string);
	} else {
		function5(result, string);
	}
}

void function1(char* string) {
	int result = 100;
	if (result <= 100) {
		function2(result, string);
	} else {
		function3(result, string);
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
		

