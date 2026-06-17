module 7458_chip (
    input p1a, p1b, p1c, p1d, p1e, p1f,
    output p1y,
    input p2a, p2b, p2c, p2d,
    output p2y );
    wire and_out_1, and_out_2, and_out_3, and_out_4;
    assign and_out_1 = (p2a & p2b); //and gate 1 
    assign and_out_2 = (p2c & p2d); //and gate 2 
    assign p2y = (and_out_1 | and_out_2); // or gate output 1 
    assign and_out_3 = (p1a & p1c & p1b); // and gate 3 
    assign and_out_4 = (p1f & p1e & p1d); // and gate 4 
    assign p1y = (and_out_3 | and_out_4); // or gate output 2 
endmodule