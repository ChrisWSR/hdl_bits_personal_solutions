module top_module(
    input [31:0] a,
    input [31:0] b,
    output [31:0] sum
);
    wire carry_high, carry_low;
    wire [15:0] high_a, high_b;
    
    add16 u_add_low(.a(a[15:0]), .b(b[15:0]), .cin(1'b0), .sum(sum[15:0]), .cout (carry_low));
    add16 u_add_high_a(.a(a[31:16]), .b(b[31:16]), .cin(1'b0), .sum(high_a), .cout (carry_high));
    add16 u_add_high_b(.a(a[31:16]), .b(b[31:16]), .cin(1'b1), .sum(high_b), .cout ());
    
    mux2to1_16bit mux_2bit (
        .a(high_a),
        .b(high_b),
        .sel(carry_low),
        .out(sum[31:16])
    );
endmodule

module mux2to1_16bit (
    input logic [15:0] a,
    input logic [15:0] b,
    input logic sel,
    output logic [15:0] out);
    
    assign out = sel ? b:a;
endmodule 