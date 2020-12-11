#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[10];
	strcpy(buf, string);
	return (0);
}

void function1(char* string);
void function2(int counter, char* string);
void function3(int counter, char* string);
void function4(int counter, char* string);
void function5();
void function6(int counter, char* string);
void function7();
void function8(int counter, char* string);
void function9(int counter, char* string);
void function10(char* string);
void function11(int counter);

void function11(int counter) {
	while (counter > 0) {
		counter--;
	}
}

void function10(char* string) {
	while (1) {
		copyData(string);
	}
}

void function9(int counter, char* string) {
	counter *= 10;
	function2(counter, string);
}

void function8(int counter, char* string) {
	counter++;
	if (counter < 100) {
		function10(string);
	} else {
		function11(counter);
	}
}

void function7() {
	int result = 100;
	for (int i = 0; i < 1000; i++) {
		result -= 2;
	}
}

void function6(int counter, char* string) {
	counter /= 10;
	if (counter < 10) {
		function8(counter, string);
	} else {
		function9(counter, string);
	}
}

void function5() {
	int result;
	for (int i = 0; i < 100; i++) {
		result = 0;
	}
}

void function4(int counter, char* string) {
	counter *= 2;
	if (counter < 100) {
		function6(counter, string);
	} else {
		function7();
	}
}

void function3(int counter, char* string) {
	while(1) {
		counter++;
	}
}

void function2(int counter, char* string) {
	counter++;
	if (counter % 2) {
		function4(counter, string);
	} else {
		function5();
	}
}

void function1(char* string) {
	int counter = 10;
	if (counter >= 10) {
		function2(counter, string);
	} else {
		function3(counter, string);
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
		

