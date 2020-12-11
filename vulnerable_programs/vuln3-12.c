#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[16];
	strcpy(buf, string);
	return (0);
}

void function1(char* string);
void function2(char* string);
void function3(int result, char* string);
void function4(char* string);
void function5(char* string);
void function6(char* string);
void function7();

void function7() {
	int count = 0;
	count++;
}

void function6(char* string) {
	copyData(string);
}

void function5(char* string) {
	int x = 100;
	while (x > 0) {
		x--;
		function4(string);
	}
	function7();
}

void function4(char* string) {
	int result = 0;
	while (result == 0) {
		copyData(string);
	}
}

void function3(int result, char* string) {
	if (result % 2 == 0) {
		result++;
	}
	function6(string);
}

void function2(char* string) {
	int result = 5;
	while (result > 0) {
		result--;
	}
	function5(string);
	while (1) {
		result++;
	}
}

void function1(char* string) {
	int result = 0;
	while (1) {
		if (result % 2 == 1) {
			function2(string);
		} else {
			function3(result, string);
		}	
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
		

