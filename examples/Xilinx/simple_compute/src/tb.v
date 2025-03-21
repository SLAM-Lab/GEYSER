`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/08/2025 06:05:33 PM
// Design Name: 
// Module Name: tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb;
    
    reg clk;
    reg start;
    wire ready;
    wire done;
    reg start1;
    wire ready1;
    wire done1;
    reg rst;
    top topa(
    .ap_clk(clk),
    .ap_rst(rst),
    .ap_start0(start),
    .ap_done0(done),
    .ap_ready0(ready),
    .ap_start1(start1),
    .ap_done1(done1),
    .ap_ready1(ready1)
    );
    

         

    initial begin 

      clk = 0;
 end
always #5 clk = ~clk;
initial begin
start = 0;
rst=0;
#20 rst=1;
#20 rst=0;
#20;
#20 start =1;
$display($time, " << Start1 >>");
wait (ready==1);
$display($time, " << Ready 1 >>");
#5 start =0;
wait(done==1);
$display($time, " << Done 1 >>");
#20 start1=1;
$display($time, " << Start 2 >>");
wait (ready1==1);
$display($time, " << Ready 2 >>");
#10 start1=0;
wait (done1==1);
$display($time, " << Done all >>");

end
endmodule
