module TEST_TESTOT(input clk, input rst);
	wire [25 - 1 : 0] allFlitsInjected;
	int totalPacketsInjected [25 - 1 : 0];
	int totalPacketsEjected [25 - 1 : 0];
	int packetsInjectedAllNodes, packetsEjectedAllNodes;


	wire [32 - 1 : 0] Node0_data_in;
	wire Node0_valid_in;
	wire Node0_ready_in;

	wire [32 - 1 : 0] Node0_data_out;
	wire Node0_valid_out;
	wire Node0_ready_out;


	wire [32 - 1 : 0] Node1_data_in;
	wire Node1_valid_in;
	wire Node1_ready_in;

	wire [32 - 1 : 0] Node1_data_out;
	wire Node1_valid_out;
	wire Node1_ready_out;


	wire [32 - 1 : 0] Node2_data_in;
	wire Node2_valid_in;
	wire Node2_ready_in;

	wire [32 - 1 : 0] Node2_data_out;
	wire Node2_valid_out;
	wire Node2_ready_out;


	wire [32 - 1 : 0] Node3_data_in;
	wire Node3_valid_in;
	wire Node3_ready_in;

	wire [32 - 1 : 0] Node3_data_out;
	wire Node3_valid_out;
	wire Node3_ready_out;


	wire [32 - 1 : 0] Node4_data_in;
	wire Node4_valid_in;
	wire Node4_ready_in;

	wire [32 - 1 : 0] Node4_data_out;
	wire Node4_valid_out;
	wire Node4_ready_out;


	wire [32 - 1 : 0] Node5_data_in;
	wire Node5_valid_in;
	wire Node5_ready_in;

	wire [32 - 1 : 0] Node5_data_out;
	wire Node5_valid_out;
	wire Node5_ready_out;


	wire [32 - 1 : 0] Node6_data_in;
	wire Node6_valid_in;
	wire Node6_ready_in;

	wire [32 - 1 : 0] Node6_data_out;
	wire Node6_valid_out;
	wire Node6_ready_out;


	wire [32 - 1 : 0] Node7_data_in;
	wire Node7_valid_in;
	wire Node7_ready_in;

	wire [32 - 1 : 0] Node7_data_out;
	wire Node7_valid_out;
	wire Node7_ready_out;


	wire [32 - 1 : 0] Node8_data_in;
	wire Node8_valid_in;
	wire Node8_ready_in;

	wire [32 - 1 : 0] Node8_data_out;
	wire Node8_valid_out;
	wire Node8_ready_out;


	wire [32 - 1 : 0] Node9_data_in;
	wire Node9_valid_in;
	wire Node9_ready_in;

	wire [32 - 1 : 0] Node9_data_out;
	wire Node9_valid_out;
	wire Node9_ready_out;


	wire [32 - 1 : 0] Node10_data_in;
	wire Node10_valid_in;
	wire Node10_ready_in;

	wire [32 - 1 : 0] Node10_data_out;
	wire Node10_valid_out;
	wire Node10_ready_out;


	wire [32 - 1 : 0] Node11_data_in;
	wire Node11_valid_in;
	wire Node11_ready_in;

	wire [32 - 1 : 0] Node11_data_out;
	wire Node11_valid_out;
	wire Node11_ready_out;


	wire [32 - 1 : 0] Node12_data_in;
	wire Node12_valid_in;
	wire Node12_ready_in;

	wire [32 - 1 : 0] Node12_data_out;
	wire Node12_valid_out;
	wire Node12_ready_out;


	wire [32 - 1 : 0] Node13_data_in;
	wire Node13_valid_in;
	wire Node13_ready_in;

	wire [32 - 1 : 0] Node13_data_out;
	wire Node13_valid_out;
	wire Node13_ready_out;


	wire [32 - 1 : 0] Node14_data_in;
	wire Node14_valid_in;
	wire Node14_ready_in;

	wire [32 - 1 : 0] Node14_data_out;
	wire Node14_valid_out;
	wire Node14_ready_out;


	wire [32 - 1 : 0] Node15_data_in;
	wire Node15_valid_in;
	wire Node15_ready_in;

	wire [32 - 1 : 0] Node15_data_out;
	wire Node15_valid_out;
	wire Node15_ready_out;


	wire [32 - 1 : 0] Node16_data_in;
	wire Node16_valid_in;
	wire Node16_ready_in;

	wire [32 - 1 : 0] Node16_data_out;
	wire Node16_valid_out;
	wire Node16_ready_out;


	wire [32 - 1 : 0] Node17_data_in;
	wire Node17_valid_in;
	wire Node17_ready_in;

	wire [32 - 1 : 0] Node17_data_out;
	wire Node17_valid_out;
	wire Node17_ready_out;


	wire [32 - 1 : 0] Node18_data_in;
	wire Node18_valid_in;
	wire Node18_ready_in;

	wire [32 - 1 : 0] Node18_data_out;
	wire Node18_valid_out;
	wire Node18_ready_out;


	wire [32 - 1 : 0] Node19_data_in;
	wire Node19_valid_in;
	wire Node19_ready_in;

	wire [32 - 1 : 0] Node19_data_out;
	wire Node19_valid_out;
	wire Node19_ready_out;


	wire [32 - 1 : 0] Node20_data_in;
	wire Node20_valid_in;
	wire Node20_ready_in;

	wire [32 - 1 : 0] Node20_data_out;
	wire Node20_valid_out;
	wire Node20_ready_out;


	wire [32 - 1 : 0] Node21_data_in;
	wire Node21_valid_in;
	wire Node21_ready_in;

	wire [32 - 1 : 0] Node21_data_out;
	wire Node21_valid_out;
	wire Node21_ready_out;


	wire [32 - 1 : 0] Node22_data_in;
	wire Node22_valid_in;
	wire Node22_ready_in;

	wire [32 - 1 : 0] Node22_data_out;
	wire Node22_valid_out;
	wire Node22_ready_out;


	wire [32 - 1 : 0] Node23_data_in;
	wire Node23_valid_in;
	wire Node23_ready_in;

	wire [32 - 1 : 0] Node23_data_out;
	wire Node23_valid_out;
	wire Node23_ready_out;


	wire [32 - 1 : 0] Node24_data_in;
	wire Node24_valid_in;
	wire Node24_ready_in;

	wire [32 - 1 : 0] Node24_data_out;
	wire Node24_valid_out;
	wire Node24_ready_out;


	noxy_top noxy_top_tb (
	.clk(clk), .rst(rst),

	.Node0_data_in(Node0_data_in), .Node0_valid_in(Node0_valid_in), .Node0_ready_in(Node0_ready_in),
	.Node0_data_out(Node0_data_out), .Node0_valid_out(Node0_valid_out), .Node0_ready_out(Node0_ready_out),

	.Node1_data_in(Node1_data_in), .Node1_valid_in(Node1_valid_in), .Node1_ready_in(Node1_ready_in),
	.Node1_data_out(Node1_data_out), .Node1_valid_out(Node1_valid_out), .Node1_ready_out(Node1_ready_out),

	.Node2_data_in(Node2_data_in), .Node2_valid_in(Node2_valid_in), .Node2_ready_in(Node2_ready_in),
	.Node2_data_out(Node2_data_out), .Node2_valid_out(Node2_valid_out), .Node2_ready_out(Node2_ready_out),

	.Node3_data_in(Node3_data_in), .Node3_valid_in(Node3_valid_in), .Node3_ready_in(Node3_ready_in),
	.Node3_data_out(Node3_data_out), .Node3_valid_out(Node3_valid_out), .Node3_ready_out(Node3_ready_out),

	.Node4_data_in(Node4_data_in), .Node4_valid_in(Node4_valid_in), .Node4_ready_in(Node4_ready_in),
	.Node4_data_out(Node4_data_out), .Node4_valid_out(Node4_valid_out), .Node4_ready_out(Node4_ready_out),

	.Node5_data_in(Node5_data_in), .Node5_valid_in(Node5_valid_in), .Node5_ready_in(Node5_ready_in),
	.Node5_data_out(Node5_data_out), .Node5_valid_out(Node5_valid_out), .Node5_ready_out(Node5_ready_out),

	.Node6_data_in(Node6_data_in), .Node6_valid_in(Node6_valid_in), .Node6_ready_in(Node6_ready_in),
	.Node6_data_out(Node6_data_out), .Node6_valid_out(Node6_valid_out), .Node6_ready_out(Node6_ready_out),

	.Node7_data_in(Node7_data_in), .Node7_valid_in(Node7_valid_in), .Node7_ready_in(Node7_ready_in),
	.Node7_data_out(Node7_data_out), .Node7_valid_out(Node7_valid_out), .Node7_ready_out(Node7_ready_out),

	.Node8_data_in(Node8_data_in), .Node8_valid_in(Node8_valid_in), .Node8_ready_in(Node8_ready_in),
	.Node8_data_out(Node8_data_out), .Node8_valid_out(Node8_valid_out), .Node8_ready_out(Node8_ready_out),

	.Node9_data_in(Node9_data_in), .Node9_valid_in(Node9_valid_in), .Node9_ready_in(Node9_ready_in),
	.Node9_data_out(Node9_data_out), .Node9_valid_out(Node9_valid_out), .Node9_ready_out(Node9_ready_out),

	.Node10_data_in(Node10_data_in), .Node10_valid_in(Node10_valid_in), .Node10_ready_in(Node10_ready_in),
	.Node10_data_out(Node10_data_out), .Node10_valid_out(Node10_valid_out), .Node10_ready_out(Node10_ready_out),

	.Node11_data_in(Node11_data_in), .Node11_valid_in(Node11_valid_in), .Node11_ready_in(Node11_ready_in),
	.Node11_data_out(Node11_data_out), .Node11_valid_out(Node11_valid_out), .Node11_ready_out(Node11_ready_out),

	.Node12_data_in(Node12_data_in), .Node12_valid_in(Node12_valid_in), .Node12_ready_in(Node12_ready_in),
	.Node12_data_out(Node12_data_out), .Node12_valid_out(Node12_valid_out), .Node12_ready_out(Node12_ready_out),

	.Node13_data_in(Node13_data_in), .Node13_valid_in(Node13_valid_in), .Node13_ready_in(Node13_ready_in),
	.Node13_data_out(Node13_data_out), .Node13_valid_out(Node13_valid_out), .Node13_ready_out(Node13_ready_out),

	.Node14_data_in(Node14_data_in), .Node14_valid_in(Node14_valid_in), .Node14_ready_in(Node14_ready_in),
	.Node14_data_out(Node14_data_out), .Node14_valid_out(Node14_valid_out), .Node14_ready_out(Node14_ready_out),

	.Node15_data_in(Node15_data_in), .Node15_valid_in(Node15_valid_in), .Node15_ready_in(Node15_ready_in),
	.Node15_data_out(Node15_data_out), .Node15_valid_out(Node15_valid_out), .Node15_ready_out(Node15_ready_out),

	.Node16_data_in(Node16_data_in), .Node16_valid_in(Node16_valid_in), .Node16_ready_in(Node16_ready_in),
	.Node16_data_out(Node16_data_out), .Node16_valid_out(Node16_valid_out), .Node16_ready_out(Node16_ready_out),

	.Node17_data_in(Node17_data_in), .Node17_valid_in(Node17_valid_in), .Node17_ready_in(Node17_ready_in),
	.Node17_data_out(Node17_data_out), .Node17_valid_out(Node17_valid_out), .Node17_ready_out(Node17_ready_out),

	.Node18_data_in(Node18_data_in), .Node18_valid_in(Node18_valid_in), .Node18_ready_in(Node18_ready_in),
	.Node18_data_out(Node18_data_out), .Node18_valid_out(Node18_valid_out), .Node18_ready_out(Node18_ready_out),

	.Node19_data_in(Node19_data_in), .Node19_valid_in(Node19_valid_in), .Node19_ready_in(Node19_ready_in),
	.Node19_data_out(Node19_data_out), .Node19_valid_out(Node19_valid_out), .Node19_ready_out(Node19_ready_out),

	.Node20_data_in(Node20_data_in), .Node20_valid_in(Node20_valid_in), .Node20_ready_in(Node20_ready_in),
	.Node20_data_out(Node20_data_out), .Node20_valid_out(Node20_valid_out), .Node20_ready_out(Node20_ready_out),

	.Node21_data_in(Node21_data_in), .Node21_valid_in(Node21_valid_in), .Node21_ready_in(Node21_ready_in),
	.Node21_data_out(Node21_data_out), .Node21_valid_out(Node21_valid_out), .Node21_ready_out(Node21_ready_out),

	.Node22_data_in(Node22_data_in), .Node22_valid_in(Node22_valid_in), .Node22_ready_in(Node22_ready_in),
	.Node22_data_out(Node22_data_out), .Node22_valid_out(Node22_valid_out), .Node22_ready_out(Node22_ready_out),

	.Node23_data_in(Node23_data_in), .Node23_valid_in(Node23_valid_in), .Node23_ready_in(Node23_ready_in),
	.Node23_data_out(Node23_data_out), .Node23_valid_out(Node23_valid_out), .Node23_ready_out(Node23_ready_out),

	.Node24_data_in(Node24_data_in), .Node24_valid_in(Node24_valid_in), .Node24_ready_in(Node24_ready_in),
	.Node24_data_out(Node24_data_out), .Node24_valid_out(Node24_valid_out), .Node24_ready_out(Node24_ready_out)

	);

	NodeVerifier #(.INDEX(0), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input0"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay0"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output0")) 
	nodeVerifier0
	(.clk(clk), .rst(rst), 
	.data_out(Node0_data_in), .valid_out(Node0_valid_in), .ready_out(Node0_ready_in), 
	.data_in(Node0_data_out), .valid_in(Node0_valid_out), .ready_in(Node0_ready_out), 
	.allFlitsInjected(allFlitsInjected[0]), 
	.totalPacketsInjected(totalPacketsInjected[0]), 
	.totalPacketsEjected(totalPacketsEjected[0]) 
	);

	NodeVerifier #(.INDEX(1), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input1"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay1"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output1")) 
	nodeVerifier1
	(.clk(clk), .rst(rst), 
	.data_out(Node1_data_in), .valid_out(Node1_valid_in), .ready_out(Node1_ready_in), 
	.data_in(Node1_data_out), .valid_in(Node1_valid_out), .ready_in(Node1_ready_out), 
	.allFlitsInjected(allFlitsInjected[1]), 
	.totalPacketsInjected(totalPacketsInjected[1]), 
	.totalPacketsEjected(totalPacketsEjected[1]) 
	);

	NodeVerifier #(.INDEX(2), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input2"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay2"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output2")) 
	nodeVerifier2
	(.clk(clk), .rst(rst), 
	.data_out(Node2_data_in), .valid_out(Node2_valid_in), .ready_out(Node2_ready_in), 
	.data_in(Node2_data_out), .valid_in(Node2_valid_out), .ready_in(Node2_ready_out), 
	.allFlitsInjected(allFlitsInjected[2]), 
	.totalPacketsInjected(totalPacketsInjected[2]), 
	.totalPacketsEjected(totalPacketsEjected[2]) 
	);

	NodeVerifier #(.INDEX(3), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input3"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay3"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output3")) 
	nodeVerifier3
	(.clk(clk), .rst(rst), 
	.data_out(Node3_data_in), .valid_out(Node3_valid_in), .ready_out(Node3_ready_in), 
	.data_in(Node3_data_out), .valid_in(Node3_valid_out), .ready_in(Node3_ready_out), 
	.allFlitsInjected(allFlitsInjected[3]), 
	.totalPacketsInjected(totalPacketsInjected[3]), 
	.totalPacketsEjected(totalPacketsEjected[3]) 
	);

	NodeVerifier #(.INDEX(4), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input4"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay4"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output4")) 
	nodeVerifier4
	(.clk(clk), .rst(rst), 
	.data_out(Node4_data_in), .valid_out(Node4_valid_in), .ready_out(Node4_ready_in), 
	.data_in(Node4_data_out), .valid_in(Node4_valid_out), .ready_in(Node4_ready_out), 
	.allFlitsInjected(allFlitsInjected[4]), 
	.totalPacketsInjected(totalPacketsInjected[4]), 
	.totalPacketsEjected(totalPacketsEjected[4]) 
	);

	NodeVerifier #(.INDEX(5), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input5"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay5"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output5")) 
	nodeVerifier5
	(.clk(clk), .rst(rst), 
	.data_out(Node5_data_in), .valid_out(Node5_valid_in), .ready_out(Node5_ready_in), 
	.data_in(Node5_data_out), .valid_in(Node5_valid_out), .ready_in(Node5_ready_out), 
	.allFlitsInjected(allFlitsInjected[5]), 
	.totalPacketsInjected(totalPacketsInjected[5]), 
	.totalPacketsEjected(totalPacketsEjected[5]) 
	);

	NodeVerifier #(.INDEX(6), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input6"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay6"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output6")) 
	nodeVerifier6
	(.clk(clk), .rst(rst), 
	.data_out(Node6_data_in), .valid_out(Node6_valid_in), .ready_out(Node6_ready_in), 
	.data_in(Node6_data_out), .valid_in(Node6_valid_out), .ready_in(Node6_ready_out), 
	.allFlitsInjected(allFlitsInjected[6]), 
	.totalPacketsInjected(totalPacketsInjected[6]), 
	.totalPacketsEjected(totalPacketsEjected[6]) 
	);

	NodeVerifier #(.INDEX(7), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input7"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay7"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output7")) 
	nodeVerifier7
	(.clk(clk), .rst(rst), 
	.data_out(Node7_data_in), .valid_out(Node7_valid_in), .ready_out(Node7_ready_in), 
	.data_in(Node7_data_out), .valid_in(Node7_valid_out), .ready_in(Node7_ready_out), 
	.allFlitsInjected(allFlitsInjected[7]), 
	.totalPacketsInjected(totalPacketsInjected[7]), 
	.totalPacketsEjected(totalPacketsEjected[7]) 
	);

	NodeVerifier #(.INDEX(8), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input8"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay8"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output8")) 
	nodeVerifier8
	(.clk(clk), .rst(rst), 
	.data_out(Node8_data_in), .valid_out(Node8_valid_in), .ready_out(Node8_ready_in), 
	.data_in(Node8_data_out), .valid_in(Node8_valid_out), .ready_in(Node8_ready_out), 
	.allFlitsInjected(allFlitsInjected[8]), 
	.totalPacketsInjected(totalPacketsInjected[8]), 
	.totalPacketsEjected(totalPacketsEjected[8]) 
	);

	NodeVerifier #(.INDEX(9), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input9"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay9"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output9")) 
	nodeVerifier9
	(.clk(clk), .rst(rst), 
	.data_out(Node9_data_in), .valid_out(Node9_valid_in), .ready_out(Node9_ready_in), 
	.data_in(Node9_data_out), .valid_in(Node9_valid_out), .ready_in(Node9_ready_out), 
	.allFlitsInjected(allFlitsInjected[9]), 
	.totalPacketsInjected(totalPacketsInjected[9]), 
	.totalPacketsEjected(totalPacketsEjected[9]) 
	);

	NodeVerifier #(.INDEX(10), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input10"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay10"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output10")) 
	nodeVerifier10
	(.clk(clk), .rst(rst), 
	.data_out(Node10_data_in), .valid_out(Node10_valid_in), .ready_out(Node10_ready_in), 
	.data_in(Node10_data_out), .valid_in(Node10_valid_out), .ready_in(Node10_ready_out), 
	.allFlitsInjected(allFlitsInjected[10]), 
	.totalPacketsInjected(totalPacketsInjected[10]), 
	.totalPacketsEjected(totalPacketsEjected[10]) 
	);

	NodeVerifier #(.INDEX(11), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input11"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay11"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output11")) 
	nodeVerifier11
	(.clk(clk), .rst(rst), 
	.data_out(Node11_data_in), .valid_out(Node11_valid_in), .ready_out(Node11_ready_in), 
	.data_in(Node11_data_out), .valid_in(Node11_valid_out), .ready_in(Node11_ready_out), 
	.allFlitsInjected(allFlitsInjected[11]), 
	.totalPacketsInjected(totalPacketsInjected[11]), 
	.totalPacketsEjected(totalPacketsEjected[11]) 
	);

	NodeVerifier #(.INDEX(12), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input12"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay12"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output12")) 
	nodeVerifier12
	(.clk(clk), .rst(rst), 
	.data_out(Node12_data_in), .valid_out(Node12_valid_in), .ready_out(Node12_ready_in), 
	.data_in(Node12_data_out), .valid_in(Node12_valid_out), .ready_in(Node12_ready_out), 
	.allFlitsInjected(allFlitsInjected[12]), 
	.totalPacketsInjected(totalPacketsInjected[12]), 
	.totalPacketsEjected(totalPacketsEjected[12]) 
	);

	NodeVerifier #(.INDEX(13), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input13"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay13"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output13")) 
	nodeVerifier13
	(.clk(clk), .rst(rst), 
	.data_out(Node13_data_in), .valid_out(Node13_valid_in), .ready_out(Node13_ready_in), 
	.data_in(Node13_data_out), .valid_in(Node13_valid_out), .ready_in(Node13_ready_out), 
	.allFlitsInjected(allFlitsInjected[13]), 
	.totalPacketsInjected(totalPacketsInjected[13]), 
	.totalPacketsEjected(totalPacketsEjected[13]) 
	);

	NodeVerifier #(.INDEX(14), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input14"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay14"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output14")) 
	nodeVerifier14
	(.clk(clk), .rst(rst), 
	.data_out(Node14_data_in), .valid_out(Node14_valid_in), .ready_out(Node14_ready_in), 
	.data_in(Node14_data_out), .valid_in(Node14_valid_out), .ready_in(Node14_ready_out), 
	.allFlitsInjected(allFlitsInjected[14]), 
	.totalPacketsInjected(totalPacketsInjected[14]), 
	.totalPacketsEjected(totalPacketsEjected[14]) 
	);

	NodeVerifier #(.INDEX(15), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input15"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay15"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output15")) 
	nodeVerifier15
	(.clk(clk), .rst(rst), 
	.data_out(Node15_data_in), .valid_out(Node15_valid_in), .ready_out(Node15_ready_in), 
	.data_in(Node15_data_out), .valid_in(Node15_valid_out), .ready_in(Node15_ready_out), 
	.allFlitsInjected(allFlitsInjected[15]), 
	.totalPacketsInjected(totalPacketsInjected[15]), 
	.totalPacketsEjected(totalPacketsEjected[15]) 
	);

	NodeVerifier #(.INDEX(16), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input16"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay16"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output16")) 
	nodeVerifier16
	(.clk(clk), .rst(rst), 
	.data_out(Node16_data_in), .valid_out(Node16_valid_in), .ready_out(Node16_ready_in), 
	.data_in(Node16_data_out), .valid_in(Node16_valid_out), .ready_in(Node16_ready_out), 
	.allFlitsInjected(allFlitsInjected[16]), 
	.totalPacketsInjected(totalPacketsInjected[16]), 
	.totalPacketsEjected(totalPacketsEjected[16]) 
	);

	NodeVerifier #(.INDEX(17), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input17"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay17"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output17")) 
	nodeVerifier17
	(.clk(clk), .rst(rst), 
	.data_out(Node17_data_in), .valid_out(Node17_valid_in), .ready_out(Node17_ready_in), 
	.data_in(Node17_data_out), .valid_in(Node17_valid_out), .ready_in(Node17_ready_out), 
	.allFlitsInjected(allFlitsInjected[17]), 
	.totalPacketsInjected(totalPacketsInjected[17]), 
	.totalPacketsEjected(totalPacketsEjected[17]) 
	);

	NodeVerifier #(.INDEX(18), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input18"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay18"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output18")) 
	nodeVerifier18
	(.clk(clk), .rst(rst), 
	.data_out(Node18_data_in), .valid_out(Node18_valid_in), .ready_out(Node18_ready_in), 
	.data_in(Node18_data_out), .valid_in(Node18_valid_out), .ready_in(Node18_ready_out), 
	.allFlitsInjected(allFlitsInjected[18]), 
	.totalPacketsInjected(totalPacketsInjected[18]), 
	.totalPacketsEjected(totalPacketsEjected[18]) 
	);

	NodeVerifier #(.INDEX(19), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input19"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay19"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output19")) 
	nodeVerifier19
	(.clk(clk), .rst(rst), 
	.data_out(Node19_data_in), .valid_out(Node19_valid_in), .ready_out(Node19_ready_in), 
	.data_in(Node19_data_out), .valid_in(Node19_valid_out), .ready_in(Node19_ready_out), 
	.allFlitsInjected(allFlitsInjected[19]), 
	.totalPacketsInjected(totalPacketsInjected[19]), 
	.totalPacketsEjected(totalPacketsEjected[19]) 
	);

	NodeVerifier #(.INDEX(20), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input20"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay20"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output20")) 
	nodeVerifier20
	(.clk(clk), .rst(rst), 
	.data_out(Node20_data_in), .valid_out(Node20_valid_in), .ready_out(Node20_ready_in), 
	.data_in(Node20_data_out), .valid_in(Node20_valid_out), .ready_in(Node20_ready_out), 
	.allFlitsInjected(allFlitsInjected[20]), 
	.totalPacketsInjected(totalPacketsInjected[20]), 
	.totalPacketsEjected(totalPacketsEjected[20]) 
	);

	NodeVerifier #(.INDEX(21), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input21"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay21"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output21")) 
	nodeVerifier21
	(.clk(clk), .rst(rst), 
	.data_out(Node21_data_in), .valid_out(Node21_valid_in), .ready_out(Node21_ready_in), 
	.data_in(Node21_data_out), .valid_in(Node21_valid_out), .ready_in(Node21_ready_out), 
	.allFlitsInjected(allFlitsInjected[21]), 
	.totalPacketsInjected(totalPacketsInjected[21]), 
	.totalPacketsEjected(totalPacketsEjected[21]) 
	);

	NodeVerifier #(.INDEX(22), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input22"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay22"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output22")) 
	nodeVerifier22
	(.clk(clk), .rst(rst), 
	.data_out(Node22_data_in), .valid_out(Node22_valid_in), .ready_out(Node22_ready_in), 
	.data_in(Node22_data_out), .valid_in(Node22_valid_out), .ready_in(Node22_ready_out), 
	.allFlitsInjected(allFlitsInjected[22]), 
	.totalPacketsInjected(totalPacketsInjected[22]), 
	.totalPacketsEjected(totalPacketsEjected[22]) 
	);

	NodeVerifier #(.INDEX(23), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input23"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay23"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output23")) 
	nodeVerifier23
	(.clk(clk), .rst(rst), 
	.data_out(Node23_data_in), .valid_out(Node23_valid_in), .ready_out(Node23_ready_in), 
	.data_in(Node23_data_out), .valid_in(Node23_valid_out), .ready_in(Node23_ready_out), 
	.allFlitsInjected(allFlitsInjected[23]), 
	.totalPacketsInjected(totalPacketsInjected[23]), 
	.totalPacketsEjected(totalPacketsEjected[23]) 
	);

	NodeVerifier #(.INDEX(24), .N(25), .VC(1), .IDENTIFIER_BITS(2), 
	.FLITS_PER_PACKET(32), 
	.PACKETS_PER_NODE(100), 
	.INPUT_TRAFFIC_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/input24"), 
	.INPUT_DELAY_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/INPUT_VECTORS/delay24"), 
	.OUTPUT_FILE("/home/ubuntu/thesis/NoxyGen/Examples/TESTTOR/Verifier/OUTPUT_VECTORS/output24")) 
	nodeVerifier24
	(.clk(clk), .rst(rst), 
	.data_out(Node24_data_in), .valid_out(Node24_valid_in), .ready_out(Node24_ready_in), 
	.data_in(Node24_data_out), .valid_in(Node24_valid_out), .ready_in(Node24_ready_out), 
	.allFlitsInjected(allFlitsInjected[24]), 
	.totalPacketsInjected(totalPacketsInjected[24]), 
	.totalPacketsEjected(totalPacketsEjected[24]) 
	);

	int N = 25;
	always_ff @(posedge clk) begin
		packetsInjectedAllNodes = 0;
		packetsEjectedAllNodes = 0;
		for(int i = 0; i < N; i++) begin
			packetsInjectedAllNodes += totalPacketsInjected[i];
			packetsEjectedAllNodes += totalPacketsEjected[i];
		end

		if(&allFlitsInjected & (packetsInjectedAllNodes == packetsEjectedAllNodes))
			$finish;
		end

endmodule
