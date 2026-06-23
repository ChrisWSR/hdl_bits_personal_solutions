module top_module ( 
    input [15:0] a, b,
    input cin,
    output cout,
    output [15:0] sum );
    wire w_fa0, w_fa1, w_fa2;
    
bcd_fadd FA0(
    .a(a[3:0]),
    .b(b[3:0]),
    .cin(cin),
	.sum(sum[3:0]),
.cout(w_fa0)
    );
bcd_fadd FA1(
    .a(a[7:4]),
    .b(b[7:4]),
	.cin(w_fa0),
	.sum(sum[7:4]),
.cout(w_fa1)
);
bcd_fadd FA2(
    .a(a[11:8]),
    .b(b[11:8]),
.cin(w_fa1),
.sum(sum[11:8]),
.cout(w_fa2)
    );    
bcd_fadd FA3(
    .a(a[15:12]),
    .b(b[15:12]),
.cin(w_fa2),
.sum(sum[15:12]),
    .cout(cout)
    );
endmodule
