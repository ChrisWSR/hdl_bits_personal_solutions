module top_module (
    input clk,
    input d, 
    input ar,   // asynchronous reset
    output reg q);
    always @(posedge clk or posedge ar) begin // this is a flip flop
        if(ar)
            q <=1'b0;
        else if (clk)
            q <= d;
    end 

endmodule
