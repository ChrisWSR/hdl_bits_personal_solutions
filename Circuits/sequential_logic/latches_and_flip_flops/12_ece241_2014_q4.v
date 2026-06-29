module top_module (
    input clk,
    input x,
    output z
); 
    wire [2:0] D;
    wire [2:0] Q;
    assign D[0] = ~Q[0] | x;
    assign D[1] = ~Q[1] & x;
    assign D[2] = Q[2] ^ x;
    always @(posedge clk) begin
        Q<=D;
    end
    assign z= ~(Q[0]|Q[1]|Q[2]);
    
endmodule
