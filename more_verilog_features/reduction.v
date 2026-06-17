module top_module (
    input [7:0] in,
    output parity); 
assign parity = ^in; // this is equivalent to doing xor to all values to check if this number is by or in by 
endmodule
