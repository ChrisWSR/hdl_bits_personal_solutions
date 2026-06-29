module top_module (
    input clk,
    input [7:0] d,
    output [7:0] q
);
// this q is a vector multiples  DDFs are created
    always @(posedge clk) begin
        q <= d;
    end 
endmodule
