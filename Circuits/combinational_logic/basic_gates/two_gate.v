module top_module (
    input in1,
    input in2,
    input in3,
    output out);
    wire w_2gate;
    assign w_2gate = ~(in1 ^ in2);
assign out = w_2gate ^ in3;
endmodule
