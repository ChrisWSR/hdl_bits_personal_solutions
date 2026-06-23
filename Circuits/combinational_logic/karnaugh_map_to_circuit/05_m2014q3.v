module top_module (
    input [4:1] x, 
    output f );
    //y = AC' + BD
    //x1 x2 = cd 
    //x3 x4 = ab
    assign f = (x[3] & ~x[1]) | (x[4] & x[2]);
endmodule
