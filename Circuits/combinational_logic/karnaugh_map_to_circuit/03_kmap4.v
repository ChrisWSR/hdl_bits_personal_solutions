module top_module(
    input a,
    input b,
    input c,
    input d,
    output out  ); 
    // the chess board form of the map can be simplified with xor cascade ecuation
assign out = a ^ b ^ c ^ d;
endmodule
