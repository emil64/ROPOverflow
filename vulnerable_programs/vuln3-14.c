#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[14];
	strcpy(buf, string);
	return (0);
}

void function9() {
	while (1) {
		printf("Processing data from function9...\n");
	}
}

void function8(char* string) {
	int result = 10;
	while (result > 0) {
		copyData(string);
		result--;
		function9();
	}
}

void function7() {
	int x = 100;
	for (int i = 0; i < 99; i++) {
		x++;
	}
}

void function6() {
	int x = 100;
	for (int i = 0; i < 99; i++) {
		x--;	
	}
}

void function5(char* string) {
	int result1 = 100, result2 = 400;
	if (result1 * result2 < 0) {
		function6();
		function7();
	} else {
		function8(string);
		function9();
	}
}

void function4() {
	int count = 0;
	while (1) {
		count++;
	}
}

void function3() {
	int count = 0;
	while (1) {
		count++;
		function4();
	}
}

void function2(char* string) {
	for (int i = 0; i < 1000; i++) {
		function5(string);
	}
}

void function1(char* string) {
	int result = 100;
	if (result > 100) {
		function3();
	} else {
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
		

