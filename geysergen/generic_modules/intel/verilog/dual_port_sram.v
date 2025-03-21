//Legal Notice: (C)2024 Altera Corporation. All rights reserved.  Your
//use of Altera Corporation's design tools, logic functions and other
//software and tools, and its AMPP partner logic functions, and any
//output files any of the foregoing (including device programming or
//simulation files), and any associated documentation or information are
//expressly subject to the terms and conditions of the Altera Program
//License Subscription Agreement or other applicable license agreement,
//including, without limitation, that your use is for the sole purpose
//of programming logic devices manufactured by Altera and sold by Altera
//or its authorized distributors.  Please refer to the applicable
//agreement for further details.

// synthesis translate_off
`timescale 1ns / 1ps
// synthesis translate_on

// turn off superfluous verilog processor warnings 
// altera message_level Level1 
// altera message_off 10034 10035 10036 10037 10230 10240 10030 13469 16735 16788 

module dual_port_sram (
    clk,
    reset,
    reset_req,
    address_0,
    byteenable_0,
    write_0,
    read_0,
    read_1,
    writedata_0,
    readdata_0,
    address_1,
    byteenable_1,
    write_1,
    writedata_1,
    readdata_1
);

  parameter INIT_FILE = "NONE";
  parameter WORD_ADD = 0;  //0 = byte addresssing, 1 = word addressing
  parameter A_WIDTH = 0;
  parameter D_WIDTH = 0;
  parameter MEM_BYTES = 4096;

  localparam WORD_SIZE = D_WIDTH/8;
  localparam MEM_WORDS = MEM_BYTES/WORD_SIZE;

  //We convert from word to byte addresses
  localparam SRAM_A_WIDTH = WORD_ADD==0?A_WIDTH-$clog2(WORD_SIZE):A_WIDTH;

  output wire [D_WIDTH-1:0] readdata_0;
  input wire [A_WIDTH-1:0] address_0;
  output wire [D_WIDTH-1:0] readdata_1;
  input wire [A_WIDTH-1:0] address_1;
  input wire [WORD_SIZE-1:0] byteenable_0;
  input wire [WORD_SIZE-1:0] byteenable_1;
  input wire clk;
  input wire reset;
  input wire reset_req;
  input wire write_0;
  input wire write_1;
  input wire [D_WIDTH-1:0] writedata_0;
  input wire [D_WIDTH-1:0] writedata_1;
  input wire read_0;
  input wire read_1;

 wire [SRAM_A_WIDTH-1:0] address_ina;
 wire [SRAM_A_WIDTH-1:0] address_inb;

  reg clken = 0;
  always @(posedge clk) begin
    if (reset) begin
      clken <= 0;
    end else begin
      clken <= 1;
    end
  end


  altsyncram the_altsyncram (
      .address_a(address_ina),
      .address_b(address_inb),
      .byteena_a(byteenable_0),
      .byteena_b(byteenable_1),
      .clock0(clk),
      .clocken0(clken),
      .data_a(writedata_0),
      .data_b(writedata_1),
      .q_a(readdata_0),
      .q_b(readdata_1),
      .wren_a(write_0),
      .wren_b(write_1)
  );


  // generate
  //   if (INIT_FILE != "NONE") begin
  //     defparam the_altsyncram.address_reg_b = "CLOCK0",
  //          the_altsyncram.byte_size = 8,
  //          the_altsyncram.byteena_reg_b = "CLOCK0",
  //          the_altsyncram.indata_reg_b = "CLOCK0",
  //          the_altsyncram.lpm_type = "altsyncram",
  //          the_altsyncram.maximum_depth = MEM_WORDS,
  //          the_altsyncram.numwords_a = MEM_WORDS,
  //          the_altsyncram.numwords_b = MEM_WORDS,
  //          the_altsyncram.operation_mode = "BIDIR_DUAL_PORT",
  //          the_altsyncram.outdata_reg_a = "UNREGISTERED",
  //          the_altsyncram.outdata_reg_b = "UNREGISTERED",
  //          the_altsyncram.ram_block_type = "M20K",
  //          the_altsyncram.read_during_write_mode_mixed_ports = "DONT_CARE",
  //          the_altsyncram.width_a = D_WIDTH,
  //          the_altsyncram.width_b = D_WIDTH,
  //          the_altsyncram.width_byteena_a = WORD_SIZE,
  //          the_altsyncram.width_byteena_b = WORD_SIZE,
  //          the_altsyncram.widthad_a = SRAM_A_WIDTH,
  //          the_altsyncram.widthad_b = SRAM_A_WIDTH,
  //          the_altsyncram.wrcontrol_wraddress_reg_b = "CLOCK0";
  //   end else begin
      defparam the_altsyncram.address_reg_b = "CLOCK0",
           the_altsyncram.byte_size = 8,
           the_altsyncram.byteena_reg_b = "CLOCK0",
           the_altsyncram.indata_reg_b = "CLOCK0",
           the_altsyncram.lpm_type = "altsyncram",
           the_altsyncram.maximum_depth = MEM_WORDS,
           the_altsyncram.numwords_a = MEM_WORDS,
           the_altsyncram.numwords_b = MEM_WORDS,
           the_altsyncram.operation_mode = "BIDIR_DUAL_PORT",
           the_altsyncram.outdata_reg_a = "UNREGISTERED",
           the_altsyncram.outdata_reg_b = "UNREGISTERED",
           the_altsyncram.ram_block_type = "M20K",
           the_altsyncram.read_during_write_mode_mixed_ports = "DONT_CARE",
           the_altsyncram.width_a = D_WIDTH,
           the_altsyncram.width_b = D_WIDTH,
           the_altsyncram.width_byteena_a = WORD_SIZE,
           the_altsyncram.width_byteena_b = WORD_SIZE,
           the_altsyncram.widthad_a = SRAM_A_WIDTH,
           the_altsyncram.widthad_b = SRAM_A_WIDTH,
           the_altsyncram.init_file = INIT_FILE,
           the_altsyncram.wrcontrol_wraddress_reg_b = "CLOCK0";
  //   end
  // endgenerate

  //Either convert a word address to a byte address or leave it be
  assign address_ina = WORD_ADD == 0 ? address_0[A_WIDTH-1:$clog2(WORD_SIZE)] : address_0;
  assign address_inb = WORD_ADD == 0 ? address_1[A_WIDTH-1:$clog2(WORD_SIZE)] : address_1;

endmodule

