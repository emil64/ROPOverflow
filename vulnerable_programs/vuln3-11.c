#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

struct object {
    int counter;
    char* string; 
};

int copyData(char *string)
{
	char buf[32];
	strcpy(buf, string);
	return (0);
}

void function1(char* string) {
    struct object newObject;
    newObject.counter = 0;
    newObject.string = malloc(sizeof(char) * strlen(string));
	strncpy(newObject.string, string, strlen(string));
    while (newObject.counter < 5) {
        newObject.counter++;
    }
    copyData(newObject.string);
    while(1) {
        newObject.counter++;
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
		

