module top_module (
    input clk,
    input resetn,
    input [1:0] byteena,
    input [15:0] d,
    output [15:0] q
);
    always @(posedge clk) begin // synchronous reset
        if(!resetn) // active-low reset 
            q <= 16'b0;
        else begin // all DFFs being trigger by the positive egde of the clk
            if(byteena[1]) begin // else not necesary because a feedback loop is begin created to keep the value of the signal
                q[15:8] <= d[15:8];
            end
            if(byteena[0]) begin
                    q[7:0] <= d[7:0];
            end 
   		end 
    end 
endmodule
