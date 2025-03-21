/*Verilog-2001 or SystemVerilog*/
module full_pipeline#(
    parameter CYCLES               = 1,
    parameter DATA_WIDTH           = 256,
    parameter SYMBOL_WIDTH         = 8,
    parameter RESPONSE_WIDTH       = 2,
    parameter HDL_ADDR_WIDTH       = 29,
    parameter BURSTCOUNT_WIDTH     = 1,

    parameter PIPELINE_COMMAND     = 1,
    parameter PIPELINE_RESPONSE    = 1,
    parameter SYNC_RESET           = 0,
    parameter USE_WRITERESPONSE    = 0,
    // --------------------------------------
    // Derived parameters
    // --------------------------------------
    parameter BYTEEN_WIDTH = DATA_WIDTH / SYMBOL_WIDTH
)

(
    input                         clk,
    input                         reset,

    output                        s0_waitrequest,
    output [DATA_WIDTH-1:0]       s0_readdata,
    output                        s0_readdatavalid,
    output                        s0_writeresponsevalid,
    output [RESPONSE_WIDTH-1:0]   s0_response,
    input  [BURSTCOUNT_WIDTH-1:0] s0_burstcount,
    input  [DATA_WIDTH-1:0]       s0_writedata,
    input  [HDL_ADDR_WIDTH-1:0]   s0_address, 
    input                         s0_write, 
    input                         s0_read, 
    input  [BYTEEN_WIDTH-1:0]     s0_byteenable, 
    input                         s0_debugaccess,
    input                         m0_waitrequest,
    input  [DATA_WIDTH-1:0]       m0_readdata,
    input                         m0_readdatavalid,
    input                         m0_writeresponsevalid,
    input  [RESPONSE_WIDTH-1:0]   m0_response,
    output [BURSTCOUNT_WIDTH-1:0] m0_burstcount,
    output [DATA_WIDTH-1:0]       m0_writedata,
    output [HDL_ADDR_WIDTH-1:0]   m0_address, 
    output                        m0_write, 
    output                        m0_read, 
    output [BYTEEN_WIDTH-1:0]     m0_byteenable,
    output                        m0_debugaccess
);

    generate
        if(CYCLES <2) begin
            HBM_interface_pipeline #(
                .DATA_WIDTH(DATA_WIDTH),
                .SYMBOL_WIDTH(SYMBOL_WIDTH),
                .RESPONSE_WIDTH(RESPONSE_WIDTH),
                .HDL_ADDR_WIDTH(HDL_ADDR_WIDTH),
                .BURSTCOUNT_WIDTH(BURSTCOUNT_WIDTH),
                .PIPELINE_COMMAND(PIPELINE_COMMAND),
                .PIPELINE_RESPONSE(PIPELINE_RESPONSE),
                .SYNC_RESET(SYNC_RESET),
                .USE_WRITERESPONSE(USE_WRITERESPONSE)
            ) my_pipe (
                .clk(clk),
                .reset(reset),
                .s0_waitrequest(s0_waitrequest),
                .s0_readdata(s0_readdata),
                .s0_readdatavalid(s0_readdatavalid),
                .s0_writeresponsevalid(s0_writeresponsevalid),
                .s0_response(s0_response),
                .s0_burstcount(s0_burstcount),
                .s0_writedata(s0_writedata),
                .s0_address(s0_address),
                .s0_write(s0_write),
                .s0_read(s0_read),
                .s0_byteenable(s0_byteenable),
                .s0_debugaccess(s0_debugaccess),
                .m0_waitrequest(m0_waitrequest),
                .m0_readdata(m0_readdata),
                .m0_readdatavalid(m0_readdatavalid),
                .m0_writeresponsevalid(m0_writeresponsevalid),
                .m0_response(m0_response),
                .m0_burstcount(m0_burstcount),
                .m0_writedata(m0_writedata),
                .m0_address(m0_address),
                .m0_write(m0_write),
                .m0_read(m0_read),
                .m0_byteenable(m0_byteenable),
                .m0_debugaccess(m0_debugaccess)
            );
        end
        else begin

            wire [0:CYCLES-2]                        R_waitrequest;
            wire [0:CYCLES-2] [DATA_WIDTH-1:0]       R_readdata;
            wire [0:CYCLES-2]                        R_readdatavalid;
            wire [0:CYCLES-2]                        R_writeresponsevalid;
            wire [0:CYCLES-2] [RESPONSE_WIDTH-1:0]   R_response;
            wire [0:CYCLES-2] [BURSTCOUNT_WIDTH-1:0] R_burstcount;
            wire [0:CYCLES-2] [DATA_WIDTH-1:0]       R_writedata;
            wire [0:CYCLES-2] [HDL_ADDR_WIDTH-1:0]   R_address;
            wire [0:CYCLES-2]                        R_write;
            wire [0:CYCLES-2]                        R_read;
            wire [0:CYCLES-2] [BYTEEN_WIDTH-1:0]     R_byteenable;

            HBM_interface_pipeline #(
                .DATA_WIDTH(DATA_WIDTH),
                .SYMBOL_WIDTH(SYMBOL_WIDTH),
                .RESPONSE_WIDTH(RESPONSE_WIDTH),
                .HDL_ADDR_WIDTH(HDL_ADDR_WIDTH),
                .BURSTCOUNT_WIDTH(BURSTCOUNT_WIDTH),
                .PIPELINE_COMMAND(PIPELINE_COMMAND),
                .PIPELINE_RESPONSE(PIPELINE_RESPONSE),
                .SYNC_RESET(SYNC_RESET),
                .USE_WRITERESPONSE(USE_WRITERESPONSE)
            ) my_pipe[0:CYCLES-1] (
                .clk(clk),
                .reset(reset),
                .s0_waitrequest({s0_waitrequest,R_waitrequest}),
                .s0_readdata({s0_readdata,R_readdata}),
                .s0_readdatavalid({s0_readdatavalid,R_readdatavalid}),
                .s0_writeresponsevalid({s0_writeresponsevalid,R_writeresponsevalid}),
                .s0_response({s0_response,R_response}),
                .s0_burstcount({s0_burstcount,R_burstcount}),
                .s0_writedata({s0_writedata,R_writedata}),
                .s0_address({s0_address,R_address}),
                .s0_write({s0_write,R_write}),
                .s0_read({s0_read,R_read}),
                .s0_byteenable({s0_byteenable,R_byteenable}),
                .m0_waitrequest({R_waitrequest,m0_waitrequest}),
                .m0_readdata({R_readdata,m0_readdata}),
                .m0_readdatavalid({R_readdatavalid,m0_readdatavalid}),
                .m0_writeresponsevalid({R_writeresponsevalid,m0_writeresponsevalid}),
                .m0_response({R_response,m0_response}),
                .m0_burstcount({R_burstcount,m0_burstcount}),
                .m0_writedata({R_writedata,m0_writedata}),
                .m0_address({R_address,m0_address}),
                .m0_write({R_write,m0_write}),
                .m0_read({R_read,m0_read}),
                .m0_byteenable({R_byteenable,m0_byteenable})
            );
        end
    endgenerate
endmodule