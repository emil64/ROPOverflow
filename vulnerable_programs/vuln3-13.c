#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <stdbool.h>

int copyData(char *string)
{
	char buf[50];
	strcpy(buf, string);
	return (0);
}

struct data {
	int result1, result2;
};

void function7() {
	int result = 0;
	for (int i = 0; i < 100; i++) {
		result++;
	}
}

void function6() {
	int result = 0;
	for (int i = 0; i < 100; i++) {
		result++;
	}
}

void function5(char* string) {
	while (1) {
		copyData(string);
	}
}

void function4() {
	int result = 0;
	for (int i = 0; i < 100; i++) {
		result++;
	}
}

void function3() {
	int result = 0;
	for (int i = 0; i < 100; i++) {
		result++;
	}
}

void function2() {
	int result = 0;
	for (int i = 0; i < 100; i++) {
		result++;
	}
}

void function1(char* string) {
	struct data newData;
	newData.result1 = 10;
	newData.result2 = 20;

	switch (newData.result1 < 10)
	{
	case true:
		switch (newData.result2 >= 20)
		{
		case true:
			function2();
			function3();
			break;
		
		default:
			function4();
			break;
		}
		break;
	
	default:
		switch (newData.result2 >= 20)
		{
		case true:
			function5(string);
			function6();
			break;
		
		default:
			function7();
			break;
		}
		break;
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
		

