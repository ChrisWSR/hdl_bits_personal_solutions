module top_module(
    input [31:0] a,
    input [31:0] b,
    input sub,
    output [31:0] sum
);
    wire logic [31:0] xor_wire;
    wire carry;
    xor_32bit u_xor_32bit(.a(b), .sub(sub), .out(xor_wire));
    add16 u_add_low(.a(a[15:0]), .b(xor_wire[15:0]), .cin(sub), .sum(sum[15:0]), .cout (carry));
    add16 u_add_high(.a(a[31:16]), .b(xor_wire[31:16]), .cin(carry), .sum(sum[31:16]), .cout ());
    
endmodule
module  xor_32bit(input logic [31:0] a,
                  input logic sub,
                  output [31:0] out);
    assign out = a ^ {32{sub}};
endmodule 
