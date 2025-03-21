//READWRITE_MODE: 0 is readonly, 1 is writeonly, 2 is readwrite
//NUM_MASTERS: Can be 2 or 4
//DWIDTH: Data width
//AWIDTH: Address width
`timescale 1 ps / 1 ps
module avalon_muxNx1 #(parameter NUM_MASTERS = 4, parameter DWIDTH = 32, parameter AWIDTH = 13,
	parameter MASTER0_READWRITE_MODE = 0,
	parameter MASTER1_READWRITE_MODE = 0,
	parameter MASTER2_READWRITE_MODE = 0,
	parameter MASTER3_READWRITE_MODE)
(
		//Avalon MM-slave interface0
		input  wire [AWIDTH-1:0]   avs_s0_address,
		input  wire                avs_s0_read,
		output wire [DWIDTH-1:0]   avs_s0_readdata,
		input  wire                avs_s0_write,
		input  wire [DWIDTH-1:0]   avs_s0_writedata,
		//Avalon MM-slave interface1
		input  wire [AWIDTH-1:0]   avs_s1_address,
		input  wire                avs_s1_read,
		output wire [DWIDTH-1:0]   avs_s1_readdata,
		input  wire                avs_s1_write,
		input  wire [DWIDTH-1:0]   avs_s1_writedata,
		//Avalon MM-slave interface2
		input  wire [AWIDTH-1:0]   avs_s2_address,
		input  wire                avs_s2_read,
		output wire [DWIDTH-1:0]   avs_s2_readdata,
		input  wire                avs_s2_write,
		input  wire [DWIDTH-1:0]   avs_s2_writedata,
		//Avalon MM-slave interface3
		input  wire [AWIDTH-1:0]   avs_s3_address,
		input  wire                avs_s3_read,
		output wire [DWIDTH-1:0]   avs_s3_readdata,
		input  wire                avs_s3_write,
		input  wire [DWIDTH-1:0]   avs_s3_writedata,
		//Avalon MM-master interface0
		output  reg [AWIDTH-1:0]  avs_m_address,
		output reg                avs_m_read,
		input wire [DWIDTH-1:0]   avs_m_readdata,
		output  reg               avs_m_write,
		output  reg [DWIDTH-1:0]  avs_m_writedata
	);

	wire master0_access;
	wire master1_access;
	wire master2_access;
	wire master3_access;
	
	//Generate logic that sets the access of each master based on their mode and if they exist.
	generate
		//Master 0 and 1 will always exist if a MUX is used. No need to check number of masters
		if (MASTER0_READWRITE_MODE == 0) begin
			assign master0_access = avs_s0_read;
		end
		else if (MASTER0_READWRITE_MODE == 1) begin
			assign master0_access = avs_s0_write;
		end
		else begin
			assign master0_access = (avs_s0_read || avs_s0_write);
		end
		
		if (MASTER1_READWRITE_MODE == 0) begin
			assign master1_access = avs_s1_read;
		end
		else if (MASTER1_READWRITE_MODE == 1) begin
			assign master1_access = avs_s1_write;
		end
		else begin
			assign master1_access = (avs_s1_read || avs_s1_write);
		end
		
		//Master 2 will only exist if NUM_MASTERS > 2
		if (NUM_MASTERS > 2) begin
			if (MASTER2_READWRITE_MODE == 0) begin
				assign master2_access = avs_s2_read;
			end
			else if (MASTER2_READWRITE_MODE == 1) begin
				assign master2_access = avs_s2_write;
			end
			else begin
				assign master2_access = (avs_s2_read || avs_s2_write);
			end
		end
		
		//Master 3 will only exist if NUM_MASTERS == 4
		if (NUM_MASTERS == 4) begin
			if (MASTER3_READWRITE_MODE == 0) begin
				assign master3_access = avs_s3_read;
			end
			else if (MASTER3_READWRITE_MODE == 1) begin
				assign master3_access = avs_s3_write;
			end
			else begin
				assign master3_access = (avs_s3_read || avs_s3_write);
			end
		end
	endgenerate

	//Generate selection logic for read, write, writedata and address, based on how many masters exist and their respective modes.
	generate
		always @(*) begin
			//Selection if number of masters is 2. Only look at masters 0 and 1.
			if (NUM_MASTERS == 2) begin
				//If master0 has access:
				if (master0_access == 1) begin
					//If readonly, then write and writedata are always 0, while read is 1.
					if (MASTER0_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					//If writeonly, pass write and writedata
					else if (MASTER0_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s0_writedata;
					end
					//If readwrite, pass all
					else begin
						avs_m_read = avs_s0_read;
						avs_m_write = avs_s0_write;
						avs_m_writedata = avs_s0_writedata;
					end
					avs_m_address = avs_s0_address;
				end
				//Similarly if master 1 has access.
				else if (master1_access == 1) begin
					if (MASTER1_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					else if (MASTER1_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s1_writedata;
					end
					else begin
						avs_m_read = avs_s1_read;
						avs_m_write = avs_s1_write;
						avs_m_writedata = avs_s1_writedata;
					end
					avs_m_address = avs_s1_address;
				end
				//If noone has access, set everything to 0.
				else begin
					avs_m_read = 0;
					avs_m_write = 0;
					avs_m_address = 0;
					avs_m_writedata = 0;
				end
			end
			//If number of masters is 3, repeat the above, but simply add one more case for master 2.
			else if (NUM_MASTERS == 3) begin
				if (master0_access == 1) begin
					//If readonly, then write and writedata are always 0, while read is 1.
					if (MASTER0_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					//If writeonly, pass write and writedata
					else if (MASTER0_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s0_writedata;
					end
					//If readwrite, pass all
					else begin
						avs_m_read = avs_s0_read;
						avs_m_write = avs_s0_write;
						avs_m_writedata = avs_s0_writedata;
					end
					avs_m_address = avs_s0_address;
				end
				//Similarly if master 1 has access.
				else if (master1_access == 1) begin
					if (MASTER1_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					else if (MASTER1_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s1_writedata;
					end
					else begin
						avs_m_read = avs_s1_read;
						avs_m_write = avs_s1_write;
						avs_m_writedata = avs_s1_writedata;
					end
					avs_m_address = avs_s1_address;
				end
				else if (master2_access == 1) begin
					if (MASTER2_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					else if (MASTER2_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s2_writedata;
					end
					else begin
						avs_m_read = avs_s2_read;
						avs_m_write = avs_s2_write;
						avs_m_writedata = avs_s2_writedata;
					end
					avs_m_address = avs_s2_address;
				end
				else begin
					avs_m_read = 0;
					avs_m_write = 0;
					avs_m_address = 0;
					avs_m_writedata = 0;
				end
			end
			//If number of masters is 4, repeat the above case, but simply add master3 as well.
			else if (NUM_MASTERS == 4) begin
				if (master0_access == 1) begin
					//If readonly, then write and writedata are always 0, while read is 1.
					if (MASTER0_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					//If writeonly, pass write and writedata
					else if (MASTER0_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s0_writedata;
					end
					//If readwrite, pass all
					else begin
						avs_m_read = avs_s0_read;
						avs_m_write = avs_s0_write;
						avs_m_writedata = avs_s0_writedata;
					end
					avs_m_address = avs_s0_address;
				end
				//Similarly if master 1 has access.
				else if (master1_access == 1) begin
					if (MASTER1_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					else if (MASTER1_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s1_writedata;
					end
					else begin
						avs_m_read = avs_s1_read;
						avs_m_write = avs_s1_write;
						avs_m_writedata = avs_s1_writedata;
					end
					avs_m_address = avs_s1_address;
				end
				else if (master2_access == 1) begin
					if (MASTER2_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					else if (MASTER2_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s2_writedata;
					end
					else begin
						avs_m_read = avs_s2_read;
						avs_m_write = avs_s2_write;
						avs_m_writedata = avs_s2_writedata;
					end
					avs_m_address = avs_s2_address;
				end
				else if (master3_access == 1) begin
					if (MASTER3_READWRITE_MODE == 0) begin
						avs_m_read = 1;
						avs_m_write = 0;
						avs_m_writedata = 0;
					end
					else if (MASTER3_READWRITE_MODE == 1) begin
						avs_m_read = 0;
						avs_m_write = 1;
						avs_m_writedata = avs_s3_writedata;
					end
					else begin
						avs_m_read = avs_s3_read;
						avs_m_write = avs_s3_write;
						avs_m_writedata = avs_s3_writedata;
					end
					avs_m_address = avs_s3_address;
				end
				else begin
					avs_m_read = 0;
					avs_m_write = 0;
					avs_m_address = 0;
					avs_m_writedata = 0;
				end
			end
		end
	endgenerate

	//Broadcast readdata to all masters that exist and are not writeonly.
	generate
		//If used, the MUX will have at least 2 masters, so not need to check if masters 0 and 1 exist.
		if (MASTER0_READWRITE_MODE != 1) begin
			assign avs_s0_readdata = avs_m_readdata;
		end
		if (MASTER1_READWRITE_MODE != 1) begin
			assign avs_s1_readdata = avs_m_readdata;
		end
		if (NUM_MASTERS > 2) begin
			if (MASTER2_READWRITE_MODE != 1) begin
				assign avs_s2_readdata = avs_m_readdata;
			end
		end
		if (NUM_MASTERS == 4) begin
			if (MASTER3_READWRITE_MODE != 1) begin
				assign avs_s3_readdata = avs_m_readdata;
			end
		end
	endgenerate

endmodule
