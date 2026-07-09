module top_module (
    input clk,
    input reset,
    input enable,
    output [3:0] Q,
    output c_enable,
    output c_load,
    output [3:0] c_d
); //


    assign c_d =4'd1; //c_load? 1'b1 : 1'b0;
    assign c_enable = enable;
    assign c_load = reset | (enable && Q == 4'd12);
    count4 the_counter (
        .clk(clk),
        .enable(c_enable),
        .load(c_load),
        .d(c_d),
        .Q(Q)
    );
    //count4 the_counter (clk, c_enable, c_load, c_d /*, ... */ );

endmodule
