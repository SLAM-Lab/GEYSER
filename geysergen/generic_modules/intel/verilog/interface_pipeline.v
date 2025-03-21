(* altera_attribute = "-name AUTO_SHIFT_REGISTER_RECOGNITION off" *) 
module interface_pipeline 
#(parameter CYCLES = 1, parameter DWIDTH = 32, parameter AWIDTH = 13, parameter READWRITE_MODE = 0) 
(
    input clk,
    input [DWIDTH-1:0]  writedata_in,
    input [AWIDTH-1:0]  address_in,
    output [DWIDTH-1:0] readdata_out,
    input               write_in,
    input               read_in,
    output [DWIDTH-1:0] writedata_out,
    output [AWIDTH-1:0] address_out,
    input [DWIDTH-1:0]  readdata_in,
    output              write_out,
    output              read_out
);

    generate if (CYCLES==0) begin : GEN_COMB_INPUT
        assign address_out = address_in;
        if (READWRITE_MODE != 0) begin
            assign write_out = write_in;
            assign writedata_out = writedata_in;
        end
        if (READWRITE_MODE != 1) begin
            assign readdata_out = readdata_in;
            assign read_out = read_in;
        end
    end 
    else begin : GEN_REG_INPUT  
        integer i;
        reg [AWIDTH-1:0] R_address [CYCLES-1:0];
        reg [DWIDTH-1:0] R_writedata [CYCLES-1:0];
        reg R_write [CYCLES-1:0];
        reg [DWIDTH-1:0] R_readdata [CYCLES-1:0];
        reg R_read [CYCLES-1:0];
        
        always @ (posedge clk) 
        begin
            R_address[0] <= address_in;
            if (READWRITE_MODE != 0) begin
                R_writedata[0] <= writedata_in;
                R_write[0] <= write_in; 
            end
            if (READWRITE_MODE != 1) begin
                R_readdata[0] <= readdata_in;
                R_read[0] <= read_in;
            end
            for(i = 1; i < CYCLES; i = i + 1) begin 
                R_address[i] <= R_address[i-1];
                if (READWRITE_MODE != 0) begin
                    R_writedata[i] <= R_writedata[i-1];
                    R_write[i] <= R_write[i-1];
                end
                if (READWRITE_MODE != 1) begin
                    R_read[i] <= R_read[i-1];
                    R_readdata[i] <= R_readdata[i-1];
                end
            end
        end
        assign address_out = R_address[CYCLES-1];
        if (READWRITE_MODE != 0) begin
            assign writedata_out = R_writedata[CYCLES-1];
            assign write_out = R_write[CYCLES-1];
        end
        if (READWRITE_MODE != 1) begin
            assign readdata_out = R_readdata[CYCLES-1];
            assign read_out = R_read[CYCLES-1];
        end
    end
    endgenerate  

endmodule