module top_module (
    input clk,
    input reset,        // Synchronous active-high reset
    output reg [3:0] q);
    always @(posedge clk) begin
        if(reset| q == 4'b1001) //reset on reset == 1 or when reaches 9 value
            q<=1'b0;
        else
            q<= q + 1'b1;
    end 
endmodule
