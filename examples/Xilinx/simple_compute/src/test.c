#include "compute.h"
#include <stdio.h>
int main(){
	printf("hello world");
	int data1[50];
	int data2[50];
	int data3[50];
	compute(data1,data2,data3);
	printf("This %d,%d,%d",data1[5],data2[5],data3[5]);
	return 0;
}
