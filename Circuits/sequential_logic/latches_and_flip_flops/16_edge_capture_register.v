module top_module (
    input clk,
    input reset,
    input [31:0] in,
    output [31:0] out
);
    reg [31:0] p_state;
    always @(posedge clk) begin
        p_state <= in;
        if (reset)
		out <= 32'd0;
        else out <= out | (~in & p_state);
    end
endmodule
