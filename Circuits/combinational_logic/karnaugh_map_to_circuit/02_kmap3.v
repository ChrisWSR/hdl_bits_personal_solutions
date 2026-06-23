module top_module(
    input a,
    input b,
    input c,
    input d,
    output out  ); 
    // 
    // a + b'c
    
    assign out = a | (~b & c ) ;
endmodule
