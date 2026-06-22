module top_module ( 
    input clk, 
    input [7:0] d, 
    input [1:0] sel, 
    output [7:0] q 
);
    wire [7:0] q1, q2,q3;
    my_dff8 dff8_ins1 (
        .clk (clk),
        .d (d),
        .q (q1)
    );
    my_dff8 dff8_ins2 (
        .clk (clk),
        .d (q1),
        .q (q2)
    );
    my_dff8 dff8_ins3 (
        .clk (clk),
        .d (q2),
        .q (q3)
    );
    mux4to1_8bits u_mux (
        .a(d), // 0 retardos
        .b(q1), // 1 retardos
        .c(q2), // 1 retardos
        .d(q3), // 1 retardos
        .sel(sel),
        .out(q) // mux output is the top_output
    );
    
endmodule


 module mux4to1_8bits (
        input [7:0] a, b, c, d,
        input [1:0] sel,
        output [7:0] out
    );
     always_comb begin
        unique case (sel) // ayuda la optimizacion y evita latches 
			2'd0: out = a;
            2'd1: out = b;
            2'd2: out = c;
            2'd3: out = d;
   
            default out = '1;// 16'hFFFF; as well could be
        endcase 
    end
 endmodule 


/// sorter solution
module top_module (
	input clk,
	input [7:0] d,
	input [1:0] sel,
	output reg [7:0] q
);

	wire [7:0] o1, o2, o3;		// output of each my_dff8
	
	// Instantiate three my_dff8s
	my_dff8 d1 ( clk, d, o1 );
	my_dff8 d2 ( clk, o1, o2 );
	my_dff8 d3 ( clk, o2, o3 );

	// This is one way to make a 4-to-1 multiplexer
	always @(*)		// Combinational always block
		case(sel)
			2'h0: q = d;
			2'h1: q = o1;
			2'h2: q = o2;
			2'h3: q = o3;
		endcase

endmodule
