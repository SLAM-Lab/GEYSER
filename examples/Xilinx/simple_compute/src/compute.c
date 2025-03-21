#include <stdio.h>
#include <string.h>
#include "compute.h"
void compute(volatile int* port0,volatile int* port1,volatile int* port2) {

#pragma HLS INTERFACE mode=bram depth=4096 latency=2 port=port1 storage_type=ram_1p
#pragma HLS INTERFACE mode=bram depth=4096 latency=2 port=port2 storage_type=ram_1p
#pragma HLS INTERFACE mode=bram depth=4096 latency=2 port=port0 storage_type=ram_2p
	for (int i = 0;i<50; i++){
		port0[i]=i;
	}
    for (int i = 0; i < 32; i++) {
        port2[2*i+1] = port0[i];
        port1[2*i] = 2*port0[i]+3;
    }
}

void compute2(volatile int* port0,volatile int* port1,volatile int* port2) {

#pragma HLS INTERFACE mode=bram depth=4096 latency=2 port=port1 storage_type=ram_1p
#pragma HLS INTERFACE mode=bram depth=4096 latency=2 port=port2 storage_type=ram_1p
#pragma HLS INTERFACE mode=bram depth=4096 latency=2 port=port0 storage_type=ram_2p
    for (int i = 0; i < 50; i++) {
        port2[i] = port0[i]+3;
        port1[i] = 2*port0[i]+3;
    }
}
