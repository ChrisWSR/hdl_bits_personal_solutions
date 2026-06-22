module top_module( 
    input [2:0] in,
    output [1:0] out );
    // more simple solution for this 
    assign out = in[0] + in[1] + in[2];
    //     integer i;
    //     always @(*) begin
    //     out = 0;
    //     for (i=0; i<3; i=i+1)
    //         out = out + in[i];
    //     	//if(in[i] == 1'b1)
    //     		//out = out + 1;
    // end 
endmodule