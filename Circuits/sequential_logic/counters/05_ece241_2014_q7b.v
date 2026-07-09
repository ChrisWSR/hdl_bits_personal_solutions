module top_module (
input clk,
input reset,
output OneHertz,
output [2:0] c_enable
);
  wire [3:0] Q0,Q1,Q2;
    assign c_enable[2] = (Q0 == 4'd9) && (Q1 == 4'd9) ; // just when clock 999
    assign c_enable[1] = (Q0 == 4'd9) ; // just when clock reach 9 
    assign c_enable[0] = 4'd1 ; // every change 
    assign OneHertz = (Q0 == 4'd9) && (Q1 == 4'd9) && (Q2 == 4'd9); // just being activate when clock change to 999 to 1000 

bcdcount counter0 (
        .clk(clk),
        .reset(reset),
        .enable(c_enable[0]),
        .Q(Q0)
    );

bcdcount counter1 (
        .clk(clk),
        .reset(reset),
    .enable(c_enable[1]),
        .Q(Q1)
    );
bcdcount counter2 (
        .clk(clk),
        .reset(reset),
    .enable(c_enable[2]),
        .Q(Q2)
    );
 endmodule 
module bcdcount (
    input clk,
    input reset,
    input enable,
    output reg [3:0] Q
);

    always @(posedge clk) begin
        if (reset) begin
            Q <= 4'd0;
        end else if (enable) begin
            if (Q == 4'd9) begin
                Q <= 4'd0;
            end else begin
                Q <= Q + 4'd1;
            end
        end
    end

endmodule
