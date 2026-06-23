module top_module(
    input a,
    input b,
    input c,
    output out  ); 
    // this problem can be solved with the negation of 0 if the only value where the expresion
    // is cero is 0 = a'b'c' the the whole expresion is out = 0' or  abc with morgan
    assign out = a | b | c;
endmodule
