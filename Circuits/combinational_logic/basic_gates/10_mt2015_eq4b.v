module top_module ( input x, input y, output z );
// with karnaught map simplification
assign z = ~x & ~y | y & x ;
// XNOR form
// assing z = (x ^~ y);
endmodule
