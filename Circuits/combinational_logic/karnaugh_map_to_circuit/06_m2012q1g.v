module top_module (
    input [4:1] x,
    output f
); 
//y = B'D' + AC' + ABD 
    //x1 x2 = c d 
    //x3 x4 = a b
    assign f = (~x[4] & ~x[2]) | (x[3] & ~x[1]) | (x[3] & x[4] & x[2]);
endmodule
