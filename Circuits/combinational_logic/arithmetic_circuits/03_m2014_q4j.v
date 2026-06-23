module full_adder( 
    input a, b, cin,
    output cout, sum );

    assign sum = a^b^cin;
    assign cout = (a&b) | (a&cin) | (b & cin);
endmodule
module top_module (
    input [3:0] x,
    input [3:0] y, 
    output [4:0] sum);
    wire w_fa0, w_fa1, w_fa2;
    full_adder FA0(
        .a(x[0]),
        .b(y[0]),
        .cin(1'b0),
        .sum(sum[0]),
        .cout(w_fa0)
    );
        full_adder FA1(
            .a(x[1]),
            .b(y[1]),
            .cin(w_fa0),
            .sum(sum[1]),
            .cout(w_fa1)
    );
            full_adder FA2(
.a(x[2]),
.b(y[2]),
.cin(w_fa1),
.sum(sum[2]),
.cout(w_fa2)
    );    
full_adder FA3(
    .a(x[3]),
    .b(y[3]),
    .cin(w_fa2),
    .sum(sum[3]),
    .cout(sum[4])
    );

    
endmodule
