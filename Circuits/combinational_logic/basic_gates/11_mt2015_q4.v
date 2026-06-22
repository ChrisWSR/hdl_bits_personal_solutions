// simplified version
module mt2015_eq4a (input x, input y, output z);
    
    assign z = (x^y) & x;
    
endmodule 
module mt2015_eq4b (input x, input y, output z);
    assign z = (x^~y);
endmodule 

module top_module (input x, input y, output z);
    wire W_a_IA1,W_a_IA2;
    wire W_b_IB1,W_b_IB2;
    wire out_or, out_and;
    mt2015_eq4a A_IA1(x , y ,W_a_IA1);
    //mt2015_eq4a A_IA2(x , y ,W_a_IA2);
    mt2015_eq4b A_IB1(x , y ,W_b_IB1);
    //mt2015_eq4b A_IB2(x , y ,W_b_IB2);
    assign out_or = W_a_IA1 | W_b_IB1;
    //assign out_and = W_a_IA2 & W_b_IB2;
    assign out_and = W_a_IA1 & W_b_IB1;
    assign z = (out_or ^  out_and);
    
endmodule

