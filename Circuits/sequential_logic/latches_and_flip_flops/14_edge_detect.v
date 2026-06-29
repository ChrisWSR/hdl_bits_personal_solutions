module top_module (
    input clk,
    input [7:0] in,
    output [7:0] pedge
);
    reg [7:0] in_p;
    always @(posedge clk)begin
        in_p <= in;
        pedge <= in & ~in_p;
        end 
endmodule
