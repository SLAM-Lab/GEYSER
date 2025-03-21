`timescale 1 ps / 1 ps
/**
This module will sync CHANNEL_COUNT done signals. 
Requires 1<=CHANNEL_COUNT<=16
*/
module sync_done 
(
	input wire fpga_clk,
  input wire reset,

	input wire done_ch0,
	input wire done_ch1,
	input wire done_ch2,
	input wire done_ch3,
	input wire done_ch4,
	input wire done_ch5,
	input wire done_ch6,
	input wire done_ch7,
	input wire done_ch8,
	input wire done_ch9,
	input wire done_ch10,
	input wire done_ch11,
	input wire done_ch12,
	input wire done_ch13,
	input wire done_ch14,
	input wire done_ch15,

	output reg done_all_channels
);
parameter CHANNEL_COUNT = 4;
localparam CHANNEL_COUNT_MINUS_ONE = CHANNEL_COUNT-1;
reg [15:0] done_state = 0;

always@(posedge fpga_clk) begin
  if (reset) begin
    done_state <= 16'h0000;
    done_all_channels <= 0;
  end else begin
    if (done_ch0 == 1) begin
      done_state[0] <= 1;
    end
    if (done_ch1 == 1 && CHANNEL_COUNT>1) begin
      done_state[1] <= 1;
    end
    if (done_ch2 == 1 && CHANNEL_COUNT>2) begin
      done_state[2] <= 1;
    end
    if (done_ch3 == 1 && CHANNEL_COUNT>3) begin
      done_state[3] <= 1;
    end
    if (done_ch4 == 1 && CHANNEL_COUNT>4) begin
      done_state[4] <= 1;
    end
    if (done_ch5 == 1 && CHANNEL_COUNT>5) begin
      done_state[5] <= 1;
    end
    if (done_ch6 == 1 && CHANNEL_COUNT>6) begin
      done_state[6] <= 1;
    end
    if (done_ch7 == 1 && CHANNEL_COUNT>7) begin
      done_state[7] <= 1;
    end
    if (done_ch8 == 1 && CHANNEL_COUNT>8) begin
      done_state[8] <= 1;
    end
    if (done_ch9 == 1 && CHANNEL_COUNT>9) begin
      done_state[9] <= 1;
    end
    if (done_ch10 == 1 && CHANNEL_COUNT>10) begin
      done_state[10] <= 1;
    end
    if (done_ch11 == 1 && CHANNEL_COUNT>11) begin
      done_state[11] <= 1;
    end
    if (done_ch12 == 1 && CHANNEL_COUNT>12) begin
      done_state[12] <= 1;
    end
    if (done_ch13 == 1 && CHANNEL_COUNT>13) begin
      done_state[13] <= 1;
    end
    if (done_ch14 == 1 && CHANNEL_COUNT>14) begin
      done_state[14] <= 1;
    end
    if (done_ch15 == 1 && CHANNEL_COUNT>15) begin
      done_state[15] <= 1;
    end
    if (done_state[CHANNEL_COUNT_MINUS_ONE:0] == {CHANNEL_COUNT{1'b1}}) begin
      done_all_channels <= 1;
      done_state <= 16'h0000;
    end
    else begin
      done_all_channels <= 0;
    end
  end
end

endmodule
