//READWRITE_MODE: 0 is readonly, 1 is writeonly, 2 is readwrite
//NUM_TARGETS: Can be 2 or 4
//DWIDTH: Data width
//MAWIDTH: Master address width
//SAWIDTH: Slave address width
//TODO: Do the same for MUX as well. Again, assume worst case of say 5 masters. Each can be readonly, writeonly or readwrite.
//Set a select signal for each based on their read and/or write signals.
//Address is then easy to select using generate ifs.
//Readdata can just get broadcast => easy.
//Writedata is also selected similarly to address.
`timescale 1 ps / 1 ps
module bram_demux #(parameter READWRITE_MODE = 2, parameter NUM_TARGETS = 2, parameter DWIDTH = 32, parameter MAWIDTH = 13, parameter SAWIDTH = 12)
(
		//BRAM target interface0
		input  wire [MAWIDTH-1:0]  bram_t0_address,
		input  wire                bram_t0_en,
		output wire [DWIDTH-1:0]   bram_t0_readdata,
		input  wire  [DWIDTH/8-1:0]              bram_t0_we,
		input  wire                bram_t0_clk,
		input  wire                bram_t0_rst,
		input  wire [DWIDTH-1:0]   bram_t0_writedata,
		//BRAM initiator interface0
		output  wire [SAWIDTH-1:0] bram_i1_address,
		output wire                bram_i1_en,
		input wire [DWIDTH-1:0]    bram_i1_readdata,
		output  wire [DWIDTH/8-1:0]              bram_i1_we,
		input  wire                bram_i1_clk,
		input  wire                bram_i1_rst,
		output  wire [DWIDTH-1:0]  bram_i1_writedata,
		//BRAM initiator interface1
		output  wire [SAWIDTH-1:0] bram_i2_address,
		output wire                bram_i2_en,
		input wire [DWIDTH-1:0]    bram_i2_readdata,
		output  wire  [DWIDTH/8-1:0]            bram_i2_we,
		input  wire                bram_i2_clk,
		input  wire                bram_i2_rst,
		output  wire [DWIDTH-1:0]  bram_i2_writedata,
		//BRAM initiator interface2
		output  wire [SAWIDTH-1:0] bram_i3_address,
		output wire                bram_i3_en,
		input wire [DWIDTH-1:0]    bram_i3_readdata,
		output  wire    [DWIDTH/8-1:0]           bram_i3_we,
		input  wire                bram_i3_clk,
		input  wire                bram_i3_rst,
		output  wire [DWIDTH-1:0]  bram_i3_writedata,
		//BRAM initiator interface3
		output  wire [SAWIDTH-1:0] bram_i4_address,
		output wire                bram_i4_en,
		input wire [DWIDTH-1:0]    bram_i4_readdata,
		output  wire  [DWIDTH/8-1:0]             bram_i4_we,
		input  wire                bram_i4_clk,
		input  wire                bram_i4_rst,
		output  wire [DWIDTH-1:0]  bram_i4_writedata
	);

	localparam integer SELECT_WIDTH = $clog2(NUM_TARGETS);
	reg [SELECT_WIDTH-1:0] select_prev = 0;

	generate
		if (READWRITE_MODE != 1) begin
			always @(posedge bram_t0_clk) begin
				if (NUM_TARGETS == 2) begin
					select_prev <= bram_t0_address[MAWIDTH-1];
				end
				else begin
					select_prev <= bram_t0_address[MAWIDTH-1:MAWIDTH-2];
				end
			end

			if (NUM_TARGETS == 2) begin
				assign bram_t0_readdata = select_prev ? bram_i2_readdata : bram_i1_readdata;
			end
			else if (NUM_TARGETS == 4) begin
				assign bram_t0_readdata = (select_prev == 2'b00) ? bram_i1_readdata : 
				                         (select_prev == 2'b01) ? bram_i2_readdata :
																 (select_prev == 2'b10) ? bram_i3_readdata : bram_i4_readdata;
			end
		end
	endgenerate

	//Generate connections based on number of slaves and readwrite mode
	generate
		if (NUM_TARGETS == 2) begin
			//Slave address is all bits but the first one
			assign bram_i1_address = bram_t0_address[MAWIDTH-2:0];
			assign bram_i2_address = bram_t0_address[MAWIDTH-2:0];
			assign bram_i1_clk=      bram_t0_clk;
			assign bram_i1_rst=      bram_t0_rst;
			assign bram_i2_clk=      bram_t0_clk;
			assign bram_i2_rst=      bram_t0_rst;
			assign bram_i1_en = (bram_t0_address[MAWIDTH-1] == 0) && bram_t0_en;
			assign bram_i2_en = (bram_t0_address[MAWIDTH-1] == 1) && bram_t0_en;
			
			//Only use write/writedata if readwrite or writeonly
			if (READWRITE_MODE != 0) begin
				assign bram_i1_we = (bram_t0_address[MAWIDTH-1] == 0)? bram_t0_we:0;
				assign bram_i1_writedata = bram_t0_writedata;
				assign bram_i2_we = (bram_t0_address[MAWIDTH-1] == 1) ? bram_t0_we:0;
				assign bram_i2_writedata = bram_t0_writedata;
			end
		end
		else begin
			//Address is all bits but the first two
			assign bram_i1_address = bram_t0_address[MAWIDTH-3:0];
			assign bram_i2_address = bram_t0_address[MAWIDTH-3:0];
			assign bram_i3_address = bram_t0_address[MAWIDTH-3:0];
			assign bram_i4_address = bram_t0_address[MAWIDTH-3:0];
			assign bram_i1_clk=      bram_t0_clk;
			assign bram_i1_rst=      bram_t0_rst;
			assign bram_i2_clk=      bram_t0_clk;
			assign bram_i2_rst=      bram_t0_rst;
			assign bram_i3_clk=      bram_t0_clk;
			assign bram_i3_rst=      bram_t0_rst;
			assign bram_i4_clk=      bram_t0_clk;
			assign bram_i4_rst=      bram_t0_rst;
			//Look at last 2 bits of address to select
			assign bram_i1_en = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b00) && bram_t0_en;
			assign bram_i2_en = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b01) && bram_t0_en;
			assign bram_i3_en = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b10) && bram_t0_en;
			assign bram_i4_en = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b11) && bram_t0_en;
			
			if (READWRITE_MODE != 0) begin
				assign bram_i1_we = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b00) ? bram_t0_we:0;
				assign bram_i2_we = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b01) ? bram_t0_we:0;
				assign bram_i3_we = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b10) ? bram_t0_we:0;
				assign bram_i4_we = (bram_t0_address[MAWIDTH-1:MAWIDTH-2] == 2'b11) ? bram_t0_we:0;
				assign bram_i1_writedata = bram_t0_writedata;
				assign bram_i2_writedata = bram_t0_writedata;
				assign bram_i3_writedata = bram_t0_writedata;
				assign bram_i4_writedata = bram_t0_writedata;
			end

		end
	endgenerate
endmodule
