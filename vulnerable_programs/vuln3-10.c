#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[300];
	strcpy(buf, string);
	return (0);
}

void function1(char* string);
void function2(int counter, char* string);
void function3(int counter, char* string);
void function4(char* string);
void function5();

void function5() {
    int counter = 0;
    counter++;
}

void function4(char* string) {
    int result = -1;
    copyData(string);
}

void function3(int counter, char* string) {
    int result = 3;
    if (result < 0) {
        function5();
    } else {
        counter++;
        function2(counter, string);
    }
}

void function2(int counter, char* string) {
    if (counter % 2 == 1) {
        function4(string);
    } else {
        function3(counter, string);
    }
}

void function1(char* string) {
    int counter = 0;
    while (1) {
        counter++;
        function2(counter, string);
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
	copyData(buffer);
	return (0);
}
		

