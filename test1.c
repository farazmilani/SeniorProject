#include <stdlib.h>
#include <stdio.h>
#include <wiringSerial.h>

void main(){
    int x,y,i=0;
    int f=0;
    int buffer[512] = {0};
    int my_controller = serialOpen("/dev/ttyUSB0",38400);

   
    printf("Waiting...\n");
    
    do{
	    x = serialGetchar(my_controller);
	    if (x != -1){
		buffer[i] = x;
		i++;
	    }
	    if (buffer[511] != 0){
		create_txt(buffer);
		for (f=0; f<512; f++){
			buffer[f]=0;
		}
		serialFlush(my_controller);
		i = 0;
		break;	
						
    	    }
    }  	
    while(1);

 
}

void create_txt(int array[]){
	FILE *fp;
	char out[] = "samp_data.txt";
	int n;
	fp = fopen(out, "w");
	if (fp == NULL){
		printf("Couldn't open\n");
		exit(0);
	}
	for (n=0; n<512; n++){
		fprintf(fp,"%d\n",array[n]);
	}
	fclose(fp);
	printf("Text file created\n");
}
//run program
//cc -o go read_serial_512.c -lwiringPi
// ./go
