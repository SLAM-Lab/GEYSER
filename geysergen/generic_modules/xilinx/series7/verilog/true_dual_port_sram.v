
module true_dual_port_sram #(
   parameter INIT_FILE = "none",
    parameter MEM_BYTES = 4096,
    parameter DATA_WIDTH           = 32,
    parameter LATENCY = 2,
   parameter CLOCKING_MODE="independent_clock", //set independent clock if a and b have different clocks common_clock = only clk a is used
   parameter MEMORY_PRIMITIVE = "block", //Use BRAM blocks by default. Could also use ultra 
    //THIS DOES NOT HANDLE UNALIGNED BYTE ADDRESSES
    parameter BYTE_ADDRESSING = 0 //HLS is stupid and will generate a bram interface with byte addressing which is not how that works. So we can fix that "decision" by adapting the addressing.
    // --------------------------------------
    // Derived parameters
    // --------------------------------------
)(
   clka,
   clkb,
   reseta,
   resetb,
   ena,
   enb,
   douta,
   doutb,
   dina,
   dinb,
   wea,
   web,
   addra,
   addrb

);

localparam MEMORY_SIZE_BITS = MEM_BYTES*8;
localparam ADDRESS_WIDTH = BYTE_ADDRESSING==0?$clog2(MEMORY_SIZE_BITS/DATA_WIDTH):$clog2(MEMORY_SIZE_BITS/8);
localparam WORD_ADDRESS_WIDTH = $clog2(MEMORY_SIZE_BITS/DATA_WIDTH);
localparam SKIP_LENGTH = $clog2(DATA_WIDTH/8);

input wire clka;
input wire clkb;
input wire reseta;
input wire resetb;
input wire ena;
input wire enb;
output wire [DATA_WIDTH-1:0]douta;
output wire [DATA_WIDTH-1:0]doutb;
input wire [DATA_WIDTH-1:0]dina;
input wire [DATA_WIDTH-1:0]dinb;
input wire [DATA_WIDTH/8-1:0] wea;
input wire [DATA_WIDTH/8-1:0] web;
input wire [ADDRESS_WIDTH-1:0] addra;
input wire [ADDRESS_WIDTH-1:0] addrb;

wire [WORD_ADDRESS_WIDTH-1:0]addra_adapt;
wire [WORD_ADDRESS_WIDTH-1:0]addrb_adapt;
assign addra_adapt = BYTE_ADDRESSING==0 ? addra : addra[ADDRESS_WIDTH-1:SKIP_LENGTH];
assign addrb_adapt = BYTE_ADDRESSING==0 ? addrb : addrb[ADDRESS_WIDTH-1:SKIP_LENGTH];

// xpm_memory_tdpram: True Dual Port RAM
// Xilinx Parameterized Macro, version 2022.2

xpm_memory_tdpram #(
   .ADDR_WIDTH_A(BYTE_ADDRESSING==0 ?ADDRESS_WIDTH:WORD_ADDRESS_WIDTH),               // DECIMAL
   .ADDR_WIDTH_B(BYTE_ADDRESSING==0 ?ADDRESS_WIDTH:WORD_ADDRESS_WIDTH),               // DECIMAL
   .AUTO_SLEEP_TIME(0),            // DECIMAL
   .BYTE_WRITE_WIDTH_A(8),        // DECIMAL
   .BYTE_WRITE_WIDTH_B(8),        // DECIMAL
   .CASCADE_HEIGHT(0),             // DECIMAL
   .CLOCKING_MODE(CLOCKING_MODE), // String
   .ECC_MODE("no_ecc"),            // String
   .MEMORY_INIT_FILE(INIT_FILE),      // String
   .MEMORY_INIT_PARAM("0"),        // String
   .MEMORY_OPTIMIZATION("true"),   // String
   .MEMORY_PRIMITIVE(MEMORY_PRIMITIVE),      // String
   .MEMORY_SIZE(MEM_BYTES*8),             // DECIMAL In Bits
   .MESSAGE_CONTROL(0),            // DECIMAL
   .READ_DATA_WIDTH_A(DATA_WIDTH),         // DECIMAL
   .READ_DATA_WIDTH_B(DATA_WIDTH),         // DECIMAL
   .READ_LATENCY_A(LATENCY),             // DECIMAL
   .READ_LATENCY_B(LATENCY),             // DECIMAL
   .READ_RESET_VALUE_A("0"),       // String
   .READ_RESET_VALUE_B("0"),       // String
   .RST_MODE_A("SYNC"),            // String
   .RST_MODE_B("SYNC"),            // String
   .SIM_ASSERT_CHK(0),             // DECIMAL; 0=disable simulation messages, 1=enable simulation messages
   .USE_EMBEDDED_CONSTRAINT(0),    // DECIMAL
   .USE_MEM_INIT(1),               // DECIMAL
   .USE_MEM_INIT_MMI(0),           // DECIMAL
   .WAKEUP_TIME("disable_sleep"),  // String
   .WRITE_DATA_WIDTH_A(DATA_WIDTH),        // DECIMAL
   .WRITE_DATA_WIDTH_B(DATA_WIDTH),        // DECIMAL
   .WRITE_MODE_A("no_change"),     // String
   .WRITE_MODE_B("no_change"),     // String
   .WRITE_PROTECT(1)               // DECIMAL
)
xpm_memory_tdpram_inst (
   .dbiterra(),             // 1-bit output: Status signal to indicate double bit error occurrence
                                    // on the data output of port A.

   .dbiterrb(),             // 1-bit output: Status signal to indicate double bit error occurrence
                                    // on the data output of port A.

   .douta(douta),                   // READ_DATA_WIDTH_A-bit output: Data output for port A read operations.
   .doutb(doutb),                   // READ_DATA_WIDTH_B-bit output: Data output for port B read operations.
   .sbiterra(sbiterra),             // 1-bit output: Status signal to indicate single bit error occurrence
                                    // on the data output of port A.

   .sbiterrb(sbiterrb),             // 1-bit output: Status signal to indicate single bit error occurrence
                                    // on the data output of port B.

   .addra(addra_adapt),                   // ADDR_WIDTH_A-bit input: Address for port A write and read operations.
   .addrb(addrb_adapt),                   // ADDR_WIDTH_B-bit input: Address for port B write and read operations.
   .clka(clka),                     // 1-bit input: Clock signal for port A. Also clocks port B when
                                    // parameter CLOCKING_MODE is "common_clock".

   .clkb(clkb),                     // 1-bit input: Clock signal for port B when parameter CLOCKING_MODE is
                                    // "independent_clock". Unused when parameter CLOCKING_MODE is
                                    // "common_clock".

   .dina(dina),                     // WRITE_DATA_WIDTH_A-bit input: Data input for port A write operations.
   .dinb(dinb),                     // WRITE_DATA_WIDTH_B-bit input: Data input for port B write operations.
   .ena(ena),                       // 1-bit input: Memory enable signal for port A. Must be high on clock
                                    // cycles when read or write operations are initiated. Pipelined
                                    // internally.

   .enb(enb),                       // 1-bit input: Memory enable signal for port B. Must be high on clock
                                    // cycles when read or write operations are initiated. Pipelined
                                    // internally.

   .injectdbiterra(1'b0), // 1-bit input: Controls double bit error injection on input data when
                                    // ECC enabled (Error injection capability is not available in
                                    // "decode_only" mode).

   .injectdbiterrb(1'b0), // 1-bit input: Controls double bit error injection on input data when
                                    // ECC enabled (Error injection capability is not available in
                                    // "decode_only" mode).

   .injectsbiterra(1'b0), // 1-bit input: Controls single bit error injection on input data when
                                    // ECC enabled (Error injection capability is not available in
                                    // "decode_only" mode).

   .injectsbiterrb(1'b0), // 1-bit input: Controls single bit error injection on input data when
                                    // ECC enabled (Error injection capability is not available in
                                    // "decode_only" mode).

   .regcea(1'b1),                 // 1-bit input: Clock Enable for the last register stage on the output
                                    // data path.

   .regceb(1'b1),                 // 1-bit input: Clock Enable for the last register stage on the output
                                    // data path.

   .rsta(reseta),                     // 1-bit input: Reset signal for the final port A output register stage.
                                    // Synchronously resets output port douta to the value specified by
                                    // parameter READ_RESET_VALUE_A.

   .rstb(resetb),                     // 1-bit input: Reset signal for the final port B output register stage.
                                    // Synchronously resets output port doutb to the value specified by
                                    // parameter READ_RESET_VALUE_B.

   .sleep(sleep),                   // 1-bit input: sleep signal to enable the dynamic power saving feature.
   .wea(wea),                       // WRITE_DATA_WIDTH_A/BYTE_WRITE_WIDTH_A-bit input: Write enable vector
                                    // for port A input data port dina. 1 bit wide when word-wide writes are
                                    // used. In byte-wide write configurations, each bit controls the
                                    // writing one byte of dina to address addra. For example, to
                                    // synchronously write only bits [15-8] of dina when WRITE_DATA_WIDTH_A
                                    // is 32, wea would be 4'b0010.

   .web(web)                        // WRITE_DATA_WIDTH_B/BYTE_WRITE_WIDTH_B-bit input: Write enable vector
                                    // for port B input data port dinb. 1 bit wide when word-wide writes are
                                    // used. In byte-wide write configurations, each bit controls the
                                    // writing one byte of dinb to address addrb. For example, to
                                    // synchronously write only bits [15-8] of dinb when WRITE_DATA_WIDTH_B
                                    // is 32, web would be 4'b0010.

);

// End of xpm_memory_tdpram_inst instantiation
endmodule