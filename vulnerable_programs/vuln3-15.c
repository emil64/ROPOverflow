#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[200];
	strcpy(buf, string);
	return (0);
}

void function1(char* string);
void function2(char* string);
void function3(char* string);
void function4(char* string);
void function5(char* string);
void function6(char* string);
void function7(char* string);
void function8(char* string);
void function9(char* string);

void function9(char* string) {
	for (int i = 0; i < 100; i++) {
		copyData(string);
		function1(string);
	}
}

void function8(char* string) {
	for (int i = 0; i < 100; i++) {
		function9(string);
	}
}

void function7(char* string) {
	for (int i = 0; i < 100; i++) {
		function8(string);
	}
}

void function6(char* string) {
	for (int i = 0; i < 100; i++) {
		function7(string);
	}
}

void function5(char* string) {
	for (int i = 0; i < 100; i++) {
		function6(string);
	}
}

void function4(char* string) {
	for (int i = 0; i < 100; i++) {
		function5(string);
	}
}

void function3(char* string) {
	for (int i = 0; i < 100; i++) {
		function4(string);
	}
}

void function2(char* string) {
	for (int i = 0; i < 100; i++) {
		function3(string);
	}
}

void function1(char* string) {
	for (int i = 0; i < 100; i++) {
		function2(string);
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
		

