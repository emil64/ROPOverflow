#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
int copyData(char *string)
{
	char buf[1];
	strcpy(buf, string);
	return (0);
}

int function(char *string) {
    int result = 0;
    for (int i = 0; i < 100; i++) {
        result++;
        copyData(string);
    }
    return result;
}

int main(int argc, char *argv[])
{
	char buffer[1000];
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
	fread(buffer, 999,1,file);
	fclose(file);
	function(buffer);
	return (0);
}
		

