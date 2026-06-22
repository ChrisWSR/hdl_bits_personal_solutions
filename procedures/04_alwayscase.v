// synthesis verilog_input_version verilog_2001
module top_module ( 
    input [2:0] sel, 
    input [3:0] data0,
    input [3:0] data1,
    input [3:0] data2,
    input [3:0] data3,
    input [3:0] data4,
    input [3:0] data5,
    output reg [3:0] out   );//

    always@(*) begin  // This is a combinational circuit
        case(sel)
			3'd0:begin
                out = data0;
            end 
            3'd1:begin
                out = data1;
            end 
            3'd2:begin
                out = data2;
            end 
            3'd3:begin
                out = data3;
            end 
            3'd4:begin
                out = data4;
            end 
            3'd5:begin
                out = data5;
            end 
            
            default: out = 4'b0;
    endcase
    end
endmodule


module top_module (
  input  logic [2:0] sel_i,
  input  logic [3:0] data0_i,
  input  logic [3:0] data1_i,
  input  logic [3:0] data2_i,
  input  logic [3:0] data3_i,
  input  logic [3:0] data4_i,
  input  logic [3:0] data5_i,
  output logic [3:0] out_o
);

  // Bloque combinacional siguiendo el estándar SystemVerilog
  always_comb begin
    unique case (sel_i) 
      3'd0:    out_o = data0_i;
      3'd1:    out_o = data1_i;
      3'd2:    out_o = data2_i;
      3'd3:    out_o = data3_i;
      3'd4:    out_o = data4_i;
      3'd5:    out_o = data5_i;
      // 'default' con ancho explícito de 4 bits y valor determinista
      default: out_o = 4'b0; 
    endcase
  end

endmodule

