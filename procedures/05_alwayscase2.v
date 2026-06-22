// synthesis verilog_input_version verilog_2001
module top_module (
    input [3:0] in,
    output reg [1:0] pos  );
//always_comb begin 
    always @(*) begin 
    if (in[0]) 
        pos = 2'd0;
	else if (in[1]) 
        pos = 2'd1;
    else if (in[2])
        pos = 2'd2;
	else if (in[3])
        pos = 2'd3;
    else
       pos = 2'd0;
end 
endmodule

// comentaries 
// in this case the less significant bit its the one with the priority
// to do it reverse the behabior its necesari to reverse the numer of the bit 
module top_module (
    input [3:0] in,
    output reg [1:0] pos
);

always @(*) begin
    if (in[3])
        pos = 2'd3;
    else if (in[2])
        pos = 2'd2;
    else if (in[1])
        pos = 2'd1;
    else
        pos = 2'd0;
end

endmodule
/// for a case solution we have haswell 
module top_module (
	input [3:0] in,
	output reg [1:0] pos
);

always @(*) begin
    case (in)

        4'h0: pos = 2'h0; // 0000 -> ningun bit activo
        4'h1: pos = 2'h0; // 0001 -> bit[0] activo -> pos=0
        4'h2: pos = 2'h1; // 0010 -> bit[1] activo -> pos=1
        4'h3: pos = 2'h0; // 0011 -> bits[1:0] activos -> gana bit[0]
        
        4'h4: pos = 2'h2; // 0100 -> bit[2] activo -> pos=2
        4'h5: pos = 2'h0; // 0101 -> bits[2] y [0] -> gana bit[0]
        4'h6: pos = 2'h1; // 0110 -> bits[2] y [1] -> gana bit[1]
        4'h7: pos = 2'h0; // 0111 -> bits[2:0] -> gana bit[0]
        
        4'h8: pos = 2'h3; // 1000 -> bit[3] activo -> pos=3
        4'h9: pos = 2'h0; // 1001 -> bits[3] y [0] -> gana bit[0]
        4'ha: pos = 2'h1; // 1010 -> bits[3] y [1] -> gana bit[1]
        4'hb: pos = 2'h0; // 1011 -> bits[3],[1],[0] -> gana bit[0]
        
        4'hc: pos = 2'h2; // 1100 -> bits[3] y [2] -> gana bit[2]
        4'hd: pos = 2'h0; // 1101 -> bits[3],[2],[0] -> gana bit[0]
        4'he: pos = 2'h1; // 1110 -> bits[3],[2],[1] -> gana bit[1]
        4'hf: pos = 2'h0; // 1111 -> todos activos -> gana bit[0]

        default: pos = 2'b0;
    endcase
end
	
	// There is an easier way to code this. See the next problem (always_casez).
	
endmodule
// Por eso:

// 0011 → 0
// 0110 → 1
// 1100 → 2
// 1000 → 3