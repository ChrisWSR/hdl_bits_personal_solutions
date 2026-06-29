module top_module (
    input clk,
    input reset,            // Synchronous reset
    input [7:0] d,
    output reg [7:0] q
);
    always @ (posedge clk )begin // synchronous behavior
        if(!reset)
        	q<=d; //Trigger by the positve side of the egde clk 
    	else
            q<=8'b0; 
    end
endmodule
