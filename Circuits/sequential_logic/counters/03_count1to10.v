module top_module (
    input clk,
    input reset,
    output reg [3:0] q);
    
    always @(posedge clk) begin
        if(reset| q == 4'b1010) //reset on reset == 1 or when reaches 10 value
            q<=1'b1;
        else
            q<= q + 1'b1;
    end 
endmodule
