//latches
module top_module (
    input d, 
    input ena,
    output q);
    always @(ena or d) begin // actalize when ena or d changes if ena changes q actualizes 
        if (ena) 
    	    q <= d;
    end

endmodule
// expected warning in Quartus synthesis 
// Warning (10240): Verilog HDL Always Construct warning at top_module.v(5): inferring latch(es)
// for variable "q", which holds its previous value in one or more paths through the always 
// construct File: /home/h/work/hdlbits.12309835/top_module.v Line: 5