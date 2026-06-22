module top_module( 
    input a, b, sel,
    output out ); 
    assign out = sel  ? b:a;
    
// assign out = (sel & b) | (~sel & a);	// Mux expressed as AND and OR
endmodule
