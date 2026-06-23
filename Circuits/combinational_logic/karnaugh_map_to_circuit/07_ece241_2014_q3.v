module top_module (
    input c,
    input d,
    output [3:0] mux_in
); 
    assign mux_in[0] = c ? 1'b1 : d ;// 00 output is 0 when c and b are 0 any other case is  1 or funtion with c+d
    assign mux_in[1] = 1'b0; // 01 always 0 
    assign mux_in[2] = d ? 1'b0 : 1'b1; // 10 not (d')
    assign mux_in[3] = c ? d: 1'b0; // 11 // and funtion in colunm 11 the output is 1 only when c1 and d1 so 
endmodule
