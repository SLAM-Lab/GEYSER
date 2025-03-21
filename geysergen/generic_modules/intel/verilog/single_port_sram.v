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

module single_port_sram (
    clk,
    reset,
    reset_req,
    address,
    byteenable,
    write,
    read,
    writedata,
    readdata
);

  parameter INIT_FILE = "NONE";
  parameter WORD_ADD = 0;  //0 = byte addresssing, 1 = word addressing
  parameter A_WIDTH = 0;
  parameter D_WIDTH = 0;
  parameter MEM_BYTES = 0;

  localparam WORD_SIZE = D_WIDTH/8;
  localparam MEM_WORDS = MEM_BYTES/WORD_SIZE;

  //We convert from word to byte addresses
  localparam SRAM_A_WIDTH = WORD_ADD==1?A_WIDTH+$clog2(WORD_SIZE):A_WIDTH;

  output wire [D_WIDTH-1:0] readdata;
  input wire [A_WIDTH-1:0] address;
  input wire [WORD_SIZE-1:0] byteenable;
  input wire clk;
  input wire reset;
  input wire reset_req;
  input wire write;
  input wire read;
  input wire [D_WIDTH-1:0] writedata;



  reg clken = 0;
  always @(posedge clk) begin
    if (reset) begin
      clken <= 0;
    end else begin
      clken <= 1;
    end
  end



  wire [A_WIDTH-1:0] address_in;
  wire               clocken0;
  assign clocken0 = clken & ~reset_req;
  altsyncram the_altsyncram (
      .address_a(address_in),
      .byteena_a(byteenable),
      .clock0(clk),
      .clocken0(clocken0),
      .data_a(writedata),
      .q_a(readdata),
      .wren_a(write)
  );


      defparam the_altsyncram.byte_size = 8,
           the_altsyncram.init_file = INIT_FILE,
           the_altsyncram.lpm_type = "altsyncram",
           the_altsyncram.numwords_a = MEM_WORDS,
           the_altsyncram.operation_mode = "SINGLE_PORT",
           the_altsyncram.outdata_reg_a = "UNREGISTERED",
           the_altsyncram.ram_block_type = "AUTO",
           the_altsyncram.read_during_write_mode_mixed_ports = "DONT_CARE",
           the_altsyncram.read_during_write_mode_port_a = "DONT_CARE",
           the_altsyncram.width_a = D_WIDTH,
           the_altsyncram.width_byteena_a = WORD_SIZE,
           the_altsyncram.widthad_a = SRAM_A_WIDTH;

  //Either convert a word address to a byte address or leave it be
  assign address_in = WORD_ADD == 0 ? address[A_WIDTH-1:$clog2(WORD_SIZE)] : address;

endmodule

