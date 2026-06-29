module top_module (
    input clk,
    input reset,
    input [7:0] d,
    output [7:0] q
);
    //always @ (posedge clk or posedge reset)begin // asynchronous behavior
    always @ (negedge clk)begin // synchronous behavior changing on low value trigger 
        if(reset)
        	q<= 8'h34;  
    	else
        	q<=d; //Trigger by the negative side of the egde clk a
    end 
endmodule
