`timescale 1 ps / 1 ps
module bram_mux #(parameter NUM_INITIATORS = 4, parameter DWIDTH = 32, parameter AWIDTH = 13,
	parameter INITIATOR0_READWRITE_MODE = 0,
	parameter INITIATOR1_READWRITE_MODE = 0,
	parameter INITIATOR2_READWRITE_MODE = 0,
	parameter INITIATOR3_READWRITE_MODE = 0)
(
		//BRAM target interface0
		input  wire [AWIDTH-1:0]   bram_t0_address,
		input  wire                bram_t0_en,
		input  wire                bram_t0_clk,
		input  wire                bram_t0_rst,
		output wire [DWIDTH-1:0]   bram_t0_readdata,
		input  wire  [DWIDTH/8-1:0]              bram_t0_we,
		input  wire [DWIDTH-1:0]   bram_t0_writedata,
		//BRAM target interface1
		input  wire [AWIDTH-1:0]   bram_t1_address,
		input  wire                bram_t1_en,
		input  wire                bram_t1_clk,
		input  wire                bram_t1_rst,
		output wire [DWIDTH-1:0]   bram_t1_readdata,
		input  wire   [DWIDTH/8-1:0]             bram_t1_we,
		input  wire [DWIDTH-1:0]   bram_t1_writedata,
		//BRAM target interface2
		input  wire [AWIDTH-1:0]   bram_t2_address,
		input  wire                bram_t2_en,
		input  wire                bram_t2_clk,
		input  wire                bram_t2_rst,
		output wire [DWIDTH-1:0]   bram_t2_readdata,
		input  wire   [DWIDTH/8-1:0]             bram_t2_we,
		input  wire [DWIDTH-1:0]   bram_t2_writedata,
		//BRAM target interface3
		input  wire [AWIDTH-1:0]   bram_t3_address,
		input  wire                bram_t3_en,
		input  wire                bram_t3_clk,
		input  wire                bram_t3_rst,
		output wire [DWIDTH-1:0]   bram_t3_readdata,
		input  wire   [DWIDTH/8-1:0]             bram_t3_we,
		input  wire [DWIDTH-1:0]   bram_t3_writedata,
		//BRAM initiator interface0
		output  reg [AWIDTH-1:0]   bram_i_address,
		output  reg                bram_i_en,
		output  reg                bram_i_clk,
		output  reg                bram_i_rst,
		input wire [DWIDTH-1:0]     bram_i_readdata,
		output  reg    [DWIDTH/8-1:0]            bram_i_we,
		output  reg [DWIDTH-1:0]   bram_i_writedata
	);

	wire initiator0_access;
	wire initiator1_access;
	wire initiator2_access;
	wire initiator3_access;
	
	//Generate logic that sets the access of each initiator based on their mode and if they exist.
	generate
		//Initiator 0 and 1 will always exist if a MUX is used. No need to check number of initiators
		if (INITIATOR0_READWRITE_MODE == 0) begin
			assign initiator0_access = bram_t0_en;
		end
		else if (INITIATOR0_READWRITE_MODE == 1) begin
			assign initiator0_access = bram_t0_we;
		end
		else begin
			assign initiator0_access = (bram_t0_en || bram_t0_we);
		end
		
		if (INITIATOR1_READWRITE_MODE == 0) begin
			assign initiator1_access = bram_t1_en;
		end
		else if (INITIATOR1_READWRITE_MODE == 1) begin
			assign initiator1_access = bram_t1_we;
		end
		else begin
			assign initiator1_access = (bram_t1_en || bram_t1_we);
		end
		
		//Initiator 2 will only exist if NUM_INITIATORS > 2
		if (NUM_INITIATORS > 2) begin
			if (INITIATOR2_READWRITE_MODE == 0) begin
				assign initiator2_access = bram_t2_en;
			end
			else if (INITIATOR2_READWRITE_MODE == 1) begin
				assign initiator2_access = bram_t2_we;
			end
			else begin
				assign initiator2_access = (bram_t2_en || bram_t2_we);
			end
		end
		
		//Initiator 3 will only exist if NUM_INITIATORS == 4
		if (NUM_INITIATORS == 4) begin
			if (INITIATOR3_READWRITE_MODE == 0) begin
				assign initiator3_access = bram_t3_en;
			end
			else if (INITIATOR3_READWRITE_MODE == 1) begin
				assign initiator3_access = bram_t3_we;
			end
			else begin
				assign initiator3_access = (bram_t3_en || bram_t3_we);
			end
		end
	endgenerate

	//Generate selection logic for read, write, 1writedata and address, based on how many initiators exist and their respective modes.
	generate
		always @(*) begin
			//Selection if number of initiators is 2. Only look at initiators 0 and 1.
			if (NUM_INITIATORS == 2) begin
				//If initiator0 has access:
				if (initiator0_access == 1) begin
					//If readonly, then write and 1writedata are always 0, while read is 1.
					if (INITIATOR0_READWRITE_MODE == 0) begin
						bram_i_we = 0;
						bram_i_writedata = 0;
					end
					//If writeonly, pass write and 1writedata
					else if (INITIATOR0_READWRITE_MODE == 1) begin
						bram_i_we = bram_t0_we;
						bram_i_writedata = bram_t0_writedata;
					end
					//If readwrite, pass all
					else begin
						bram_i_we = bram_t0_we;
						bram_i_writedata = bram_t0_writedata;
					end
					bram_i_en = bram_t0_en;
					bram_i_clk = bram_t0_clk;
					bram_i_rst = bram_t0_rst;
					bram_i_address = bram_t0_address;
				end
				//Similarly if initiator 1 has access.
				else if (initiator1_access == 1) begin
					if (INITIATOR1_READWRITE_MODE == 0) begin
						bram_i_we = 0;
						bram_i_writedata = 0;
					end
					else if (INITIATOR1_READWRITE_MODE == 1) begin
						bram_i_we = bram_t1_we;
						bram_i_writedata = bram_t1_writedata;
					end
					else begin
						
						bram_i_we = bram_t1_we;
						bram_i_writedata = bram_t1_writedata;
					end
					bram_i_en = bram_t1_en;
					bram_i_address = bram_t1_address;
					bram_i_clk = bram_t1_clk;
					bram_i_rst = bram_t1_rst;
				end
				//If noone has access, set everything to 0.
				else begin
					bram_i_en = 0;
					bram_i_we = 0;
					bram_i_address = 0;
					bram_i_writedata = 0;
					bram_i_clk = 0;
					bram_i_rst = 0;
				end
			end
			//If number of initiators is 3, repeat the above, but simply add one more case for initiator 2.
			else if (NUM_INITIATORS == 3) begin
				if (initiator0_access == 1) begin
					//If readonly, then write and 1writedata are always 0, while read is 1.
					if (INITIATOR0_READWRITE_MODE == 0) begin
						bram_i_we = 0;
						bram_i_writedata = 0;
					end
					//If writeonly, pass write and 1writedata
					else if (INITIATOR0_READWRITE_MODE == 1) begin
						bram_i_we = bram_t0_we;
						bram_i_writedata = bram_t0_writedata;
					end
					//If readwrite, pass all
					else begin
						bram_i_we = bram_t0_we;
						bram_i_writedata = bram_t0_writedata;
					end
					bram_i_en = bram_t0_en;
					bram_i_clk = bram_t0_clk;
					bram_i_rst = bram_t0_rst;
					bram_i_address = bram_t0_address;
				end
				//Similarly if initiator 1 has access.
				else if (initiator1_access == 1) begin
					if (INITIATOR1_READWRITE_MODE == 0) begin
						bram_i_we = 0;
						bram_i_writedata = 0;
					end
					else if (INITIATOR1_READWRITE_MODE == 1) begin
						bram_i_we = bram_t1_we;
						bram_i_writedata = bram_t1_writedata;
					end
					else begin
						
						bram_i_we = bram_t1_we;
						bram_i_writedata = bram_t1_writedata;
					end
					bram_i_en = bram_t1_en;
					bram_i_address = bram_t1_address;
					bram_i_clk = bram_t1_clk;
					bram_i_rst = bram_t1_rst;
				end
				else if (initiator2_access == 1) begin
					if (INITIATOR2_READWRITE_MODE == 0) begin
						bram_i_writedata = 0;
					end
					else if (INITIATOR2_READWRITE_MODE == 1) begin
						bram_i_we = bram_t2_we;
						bram_i_writedata = bram_t2_writedata;
					end
					else begin
						bram_i_we = bram_t2_we;
						bram_i_writedata = bram_t2_writedata;
					end
					bram_i_en = bram_t2_en;
					bram_i_address = bram_t2_address;
					bram_i_clk = bram_t2_clk;
					bram_i_rst = bram_t2_rst;
				end
				else begin
					bram_i_en = 0;
					bram_i_we = 0;
					bram_i_address = 0;
					bram_i_writedata = 0;
					bram_i_clk = 0;
					bram_i_rst = 0;
				end
			end
			//If number of initiators is 4, repeat the above case, but simply add initiator3 as well.
			else if (NUM_INITIATORS == 4) begin
				if (initiator0_access == 1) begin
					//If readonly, then write and 1writedata are always 0, while read is 1.
					if (INITIATOR0_READWRITE_MODE == 0) begin
						bram_i_we = 0;
						bram_i_writedata = 0;
					end
					//If writeonly, pass write and 1writedata
					else if (INITIATOR0_READWRITE_MODE == 1) begin
						bram_i_we = bram_t0_we;
						bram_i_writedata = bram_t0_writedata;
					end
					//If readwrite, pass all
					else begin
						bram_i_we = bram_t0_we;
						bram_i_writedata = bram_t0_writedata;
					end
					bram_i_en = bram_t0_en;
					bram_i_clk = bram_t0_clk;
					bram_i_rst = bram_t0_rst;
					bram_i_address = bram_t0_address;
				end
				//Similarly if initiator 1 has access.
				else if (initiator1_access == 1) begin
					if (INITIATOR1_READWRITE_MODE == 0) begin
						bram_i_we = 0;
						bram_i_writedata = 0;
					end
					else if (INITIATOR1_READWRITE_MODE == 1) begin
						bram_i_we = bram_t1_we;
						bram_i_writedata = bram_t1_writedata;
					end
					else begin
						
						bram_i_we = bram_t1_we;
						bram_i_writedata = bram_t1_writedata;
					end
					bram_i_en = bram_t1_en;
					bram_i_address = bram_t1_address;
					bram_i_clk = bram_t1_clk;
					bram_i_rst = bram_t1_rst;
				end
				else if (initiator2_access == 1) begin
					if (INITIATOR2_READWRITE_MODE == 0) begin
						bram_i_writedata = 0;
					end
					else if (INITIATOR2_READWRITE_MODE == 1) begin
						bram_i_we = bram_t2_we;
						bram_i_writedata = bram_t2_writedata;
					end
					else begin
						bram_i_we = bram_t2_we;
						bram_i_writedata = bram_t2_writedata;
					end
					bram_i_en = bram_t2_en;
					bram_i_address = bram_t2_address;
					bram_i_clk = bram_t2_clk;
					bram_i_rst = bram_t2_rst;
				end

				else if (initiator3_access == 1) begin
					if (INITIATOR3_READWRITE_MODE == 0) begin
						bram_i_writedata = 0;
					end
					else begin
						bram_i_we = bram_t3_we;
						bram_i_writedata = bram_t3_writedata;
					end
					bram_i_en = bram_t3_en;
					bram_i_address = bram_t3_address;
					bram_i_clk = bram_t3_clk;
					bram_i_rst = bram_t3_rst;
				end
				else begin
					bram_i_en = 0;
					bram_i_we = 0;
					bram_i_address = 0;
					bram_i_writedata = 0;
					bram_i_clk = 0;
					bram_i_rst = 0;
				end
			end
		end
	endgenerate

	//Broadcast readdata to all initiators that exist and are not writeonly.
	generate
		//If used, the MUX will have at least 2 initiators, so not need to check if initiators 0 and 1 exist.
		if (INITIATOR0_READWRITE_MODE != 1) begin
			assign bram_t0_readdata = bram_i_readdata;
		end
		if (INITIATOR1_READWRITE_MODE != 1) begin
			assign bram_t1_readdata = bram_i_readdata;
		end
		if (NUM_INITIATORS > 2) begin
			if (INITIATOR2_READWRITE_MODE != 1) begin
				assign bram_t2_readdata = bram_i_readdata;
			end
		end
		if (NUM_INITIATORS == 4) begin
			if (INITIATOR3_READWRITE_MODE != 1) begin
				assign bram_t3_readdata = bram_i_readdata;
			end
		end
	endgenerate

endmodule
