module top_module (
    input clk,
    input reset,   // Synchronous active-high reset
    output [3:1] ena,
    output [15:0] q);
    
    
    assign ena[3] = (q[3:0]==  4'd9) && (q[7:4] == 4'd9) && (q[11:8] == 4'd9) ; // just when clock 999
    assign ena[2] = (q[3:0] == 4'd9) && (q[7:4] == 4'd9) ; // just when clock 99
    assign ena[1] = (q[3:0] == 4'd9) ; // just when clock reach 9 
    
bcdcount units (
        .clk(clk),
        .reset(reset),
    .enable(1'b1),
    .Q(q[3:0])
    );

bcdcount tens (
        .clk(clk),
        .reset(reset),
    .enable(ena[1]),
    .Q(q[7:4])
    );
bcdcount hundreds (
        .clk(clk),
        .reset(reset),
    .enable(ena[2]),
    .Q(q[11:8])
    );
bcdcount thousands(
        .clk(clk),
        .reset(reset),
    .enable(ena[3]),
    .Q(q[15:12])
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
