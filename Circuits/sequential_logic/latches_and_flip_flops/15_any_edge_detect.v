module top_module (
    input clk,
    input [7:0] in,
    output [7:0] anyedge
);
    reg [7:0] in_p;
    always @(posedge clk)begin
        in_p <= in; //save previous state
        anyedge <= in ^ in_p; // xor operation for any chance bit to bit
    end
endmodule
