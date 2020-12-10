#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[12];
	strcpy(buf, string);
	return (0);
}

void function4(char* string) {
    while(1) {
        copyData(string);
    }
}

void function3(char* string) {
    int count = 0;
    for (int i = 0; i < 1000; i++) {
        count += 1;
        function4(string);
    }
    return;
}

void function2(char* string) {
    int result = 10;
    result += 1;
    return;
}

void function1(char* string) {
    int result = 3;
    if (result % 2) {
        function3(string);
    } else {
        function2(string);
    }
    return;
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
		

