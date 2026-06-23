module top_module(
    input a,
    input b,
    input c,
    input d,
    output out  ); 
 
 //   A'D'+ACD+B'C'+BCD
    assign out = (~a&~d)  | (a&c&d) | (~b&~c) | (b&c&d);

    
endmodule
