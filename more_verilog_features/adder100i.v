module one_bit_fa(
    input a,b,
    input cin,
    output cout, sum);
    assign sum = a^b^cin;
    assign cout = (a&b) | (a&cin) | (b & cin);
endmodule

module top_module( 
    input [99:0] a, b,
    input cin,
    output [99:0] cout,
    output [99:0] sum );
	genvar i;
    one_bit_fa fa1(a[0],b[0],cin,cout[0],sum[0]);
    
    
    generate 
        for (i=1; i<100;i=i+1) begin : full_adder_block
            one_bit_fa fa1(a[i],b[i],cout[i-1],cout[i],sum[i]);
        end
    endgenerate 
endmodule
