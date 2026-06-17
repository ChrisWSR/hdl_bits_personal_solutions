// synthesis verilog_input_version verilog_2001
module top_module (
    input [15:0] scancode,
    output reg left,
    output reg down,
    output reg right,
    output reg up  ); 

// Scancode [15:0]	Arrow key
// 16'he06b	left arrow
// 16'he072	down arrow
// 16'he074	right arrow
// 16'he075	up arrow
// Anything else	none
always @(*) begin
up = 1'b0; 
down = 1'b0;
left = 1'b0;
right = 1'b0;

case(scancode)
    16'he06b: left = 1'b1;
    16'he072: down = 1'b1;
    16'he074: right= 1'b1;
    16'he075: up = 1'b1;
    default
     
    endcase
end 

endmodule
