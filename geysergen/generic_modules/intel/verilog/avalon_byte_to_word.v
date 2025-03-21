`timescale 1 ns / 1 ns


module Avalon_Byte_to_Word 
#(
    parameter DATA_WIDTH           = 32,
    parameter SYMBOL_WIDTH         = 8,
    parameter ADDR_WIDTH       = 10,
    parameter BURSTCOUNT_WIDTH     = 1,

    // --------------------------------------
    // Derived parameters
    // --------------------------------------
    parameter BYTEEN_WIDTH = DATA_WIDTH / SYMBOL_WIDTH
)
(
    input clock,
    input reset,
    output                        s0_waitrequest,
    output [DATA_WIDTH-1:0]       s0_readdata,
    output                        s0_readdatavalid,
    input  [BURSTCOUNT_WIDTH-1:0] s0_burstcount,
    input  [DATA_WIDTH-1:0]       s0_writedata,
    input  [ADDR_WIDTH-1:0]   s0_address, 
    input                         s0_write, 
    input                         s0_read, 
    input  [BYTEEN_WIDTH-1:0]     s0_byteenable, 

    input                         m0_waitrequest,
    input  [DATA_WIDTH-1:0]       m0_readdata,
    input                         m0_readdatavalid,
    output [BURSTCOUNT_WIDTH-1:0] m0_burstcount,
    output [DATA_WIDTH-1:0]       m0_writedata,
    output [ADDR_WIDTH-1-$clog2(BYTEEN_WIDTH):0]   m0_address, 
    output                        m0_write, 
    output                        m0_read, 
    output [BYTEEN_WIDTH-1:0]     m0_byteenable
);
    assign s0_waitrequest = m0_waitrequest;
    assign s0_readdata = m0_readdata;
    assign s0_readdatavalid =m0_readdatavalid;
    assign m0_burstcount=s0_burstcount;
    assign m0_writedata=s0_writedata;
    assign m0_address=s0_address[ADDR_WIDTH-1:$clog2(BYTEEN_WIDTH)];
    assign m0_write=s0_write;
    assign m0_read=s0_read;
    assign m0_byteenable=s0_byteenable;
endmodule