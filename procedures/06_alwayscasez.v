// xxxxxxxx1 → 0
// xxxxxxx10 → 1
// xxxxxx100 → 2
// xxxxx1000 → 3
// xxxx10000 → 4
// xxx100000 → 5
// xx1000000 → 6
// x10000000 → 7
// synthesis verilog_input_version verilog_2001
module top_module (
    input [7:0] in,
    output reg [2:0] pos );
    always @(*) begin
        casez(in)
            8'bzzzz_zzz1: pos = 3'd0;
            8'bzzzz_zz1z: pos = 3'd1;
            8'bzzzz_z1zz: pos = 3'd2;
            8'bzzzz_1zzz: pos = 3'd3;
            8'bzzz1_zzzz: pos = 3'd4; //  8'b10010000 should output 3'd4, because bit[4] is fi
            8'bzz1z_zzzz: pos = 3'd5;
            8'bz1zz_zzzz: pos = 3'd6;
            8'b1zzz_zzzz: pos = 3'd7;
            default: pos = 3'd0;
        endcase
    end 
endmodule
