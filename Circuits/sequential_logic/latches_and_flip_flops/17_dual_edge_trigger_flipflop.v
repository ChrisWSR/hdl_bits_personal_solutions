module top_module (
    input clk,
    input d,
    output q
);
reg tmp1, tmp2;
    always @(posedge clk)
        begin tmp1 <=d;end // save the status on positive edge
    always @(negedge clk)
        begin tmp2 <=d;end // save the status on negative edge 
    always @(clk) begin
        if(clk) // chance with the clock the output
            q <= tmp1;
        else
            q <=tmp2;
		end
endmodule
