//READWRITE_MODE: 0 is readonly, 1 is writeonly, 2 is readwrite
//NUM_SLAVES: Can be 2 or 4
//DWIDTH: Data width
//MAWIDTH: Master address width
//SAWIDTH: Slave address width
//TODO: Do the same for MUX as well. Again, assume worst case of say 5 masters. Each can be readonly, writeonly or readwrite.
//Set a select signal for each based on their read and/or write signals.
//Address is then easy to select using generate ifs.
//Readdata can just get broadcast => easy.
//Writedata is also selected similarly to address.
`timescale 1 ps / 1 ps
module avalon_demux1xN #(parameter READWRITE_MODE = 2, parameter NUM_SLAVES = 2, parameter DWIDTH = 32, parameter MAWIDTH = 13, parameter SAWIDTH = 12)
(
		//Avalon MM-slave interface0
		input  wire [MAWIDTH-1:0]  avs_s0_address,
		input  wire                avs_s0_read,
		output wire [DWIDTH-1:0]   avs_s0_readdata,
		input  wire                avs_s0_write,
		input  wire [DWIDTH-1:0]   avs_s0_writedata,
		//Avalon MM-master interface0
		output  wire [SAWIDTH-1:0] avs_m1_address,
		output wire                avs_m1_read,
		input wire [DWIDTH-1:0]  	 avs_m1_readdata,
		output  wire               avs_m1_write,
		output  wire [DWIDTH-1:0]  avs_m1_writedata,
		//Avalon MM-master interface1
		output  wire [SAWIDTH-1:0] avs_m2_address,
		output wire                avs_m2_read,
		input wire [DWIDTH-1:0]  	 avs_m2_readdata,
		output  wire               avs_m2_write,
		output  wire [DWIDTH-1:0]  avs_m2_writedata,
		//Avalon MM-master interface2
		output  wire [SAWIDTH-1:0] avs_m3_address,
		output wire                avs_m3_read,
		input wire [DWIDTH-1:0]  	 avs_m3_readdata,
		output  wire               avs_m3_write,
		output  wire [DWIDTH-1:0]  avs_m3_writedata,
		//Avalon MM-master interface3
		output  wire [SAWIDTH-1:0] avs_m4_address,
		output wire                avs_m4_read,
		input wire [DWIDTH-1:0]  	 avs_m4_readdata,
		output  wire               avs_m4_write,
		output  wire [DWIDTH-1:0]  avs_m4_writedata,
		input  wire        clock
	);

	localparam integer SELECT_WIDTH = $clog2(NUM_SLAVES);
	reg [SELECT_WIDTH-1:0] select_prev = 0;

	generate
		if (READWRITE_MODE != 1) begin
			always @(posedge clock) begin
				if (NUM_SLAVES == 2) begin
					select_prev <= avs_s0_address[MAWIDTH-1];
				end
				else begin
					select_prev <= avs_s0_address[MAWIDTH-1:MAWIDTH-2];
				end
			end

			if (NUM_SLAVES == 2) begin
				assign avs_s0_readdata = select_prev ? avs_m2_readdata : avs_m1_readdata;
			end
			else if (NUM_SLAVES == 4) begin
				assign avs_s0_readdata = (select_prev == 2'b00) ? avs_m1_readdata : 
				                         (select_prev == 2'b01) ? avs_m2_readdata :
																 (select_prev == 2'b10) ? avs_m3_readdata : avs_m4_readdata;
			end
		end
	endgenerate

	//Generate connections based on number of slaves and readwrite mode
	generate
		if (NUM_SLAVES == 2) begin
			//Slave address is all bits but the first one
			assign avs_m1_address = avs_s0_address[MAWIDTH-2:0];
			assign avs_m2_address = avs_s0_address[MAWIDTH-2:0];
			
			if (READWRITE_MODE != 1) begin
				//Only look at last bit to select
				assign avs_m1_read = (avs_s0_address[MAWIDTH-1] == 0) && avs_s0_read;
				assign avs_m2_read = (avs_s0_address[MAWIDTH-1] == 1) && avs_s0_read;
			end
			
			//Only use write/writedata if readwrite or writeonly
			if (READWRITE_MODE != 0) begin
				assign avs_m1_write = (avs_s0_address[MAWIDTH-1] == 0) && avs_s0_write;
				assign avs_m1_writedata = avs_s0_writedata;
				assign avs_m2_write = (avs_s0_address[MAWIDTH-1] == 1) && avs_s0_write;
				assign avs_m2_writedata = avs_s0_writedata;
			end
		end
		else begin
			//Address is all bits but the first two
			assign avs_m1_address = avs_s0_address[MAWIDTH-3:0];
			assign avs_m2_address = avs_s0_address[MAWIDTH-3:0];
			assign avs_m3_address = avs_s0_address[MAWIDTH-3:0];
			assign avs_m4_address = avs_s0_address[MAWIDTH-3:0];
			
			//Look at last 2 bits of address to select
			if (READWRITE_MODE != 1) begin
				assign avs_m1_read = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b00) && avs_s0_read;
				assign avs_m2_read = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b01) && avs_s0_read;
				assign avs_m3_read = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b10) && avs_s0_read;
				assign avs_m4_read = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b11) && avs_s0_read;
			end
			
			if (READWRITE_MODE != 0) begin
				assign avs_m1_write = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b00) && avs_s0_write;
				assign avs_m2_write = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b01) && avs_s0_write;
				assign avs_m3_write = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b10) && avs_s0_write;
				assign avs_m4_write = (avs_s0_address[MAWIDTH-1:MAWIDTH-2] == 2'b11) && avs_s0_write;
				assign avs_m1_writedata = avs_s0_writedata;
				assign avs_m2_writedata = avs_s0_writedata;
				assign avs_m3_writedata = avs_s0_writedata;
				assign avs_m4_writedata = avs_s0_writedata;
			end

		end
	endgenerate
endmodule
