`default_nettype none
module top_module(
    input a,
    input b,
    input c,
    input d,
    output out,
    output out_n   ); 
    wire wire_a;
    wire wire_b;
    assign wire_a = (a & b);
    assign wire_b = (c & d);   
    assign out = (wire_a | wire_b);     
	assign out_n = ~out;
endmodule
