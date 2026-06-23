// A single-output digital system with four inputs (a,b,c,d)
// generates a logic-1 when 2, 7, or 15 appears on the inputs, 
// and a logic-0 when 0, 1, 4, 5, 6, 9, 10, 13, or 14 appears. 
// The input conditions for the numbers 3, 8, 11, and 12 never 
// occur in this system. For example, 7 corresponds to a,b,c,d
// being set to 0,1,1,1, respectively.
// SUM of PRODUCTS
// Map
// C.D	C.D	C.D	C.D
// A.B	0	0	x	1
// A.B	0	0	1	0
// A.B	x	0	x	0
// A.B	x	0	x	0
// Map Layout
// C.D	C.D	C.D	C.D
// A.B	0	1	3	2
// A.B	4	5	7	6
// A.B	12	13	15	14
// A.B	8	9	11	10
// Groups
// (3,7,11,15)	C.D
// (2,3)	A.B.C
// y = CD + A'B'C
module top_module (
    input a,
    input b,
    input c,
    input d,
    output out_sop,
    output out_pos
); 
    assign out_sop = c & (~a | d) & (~b | d);
    assign out_pos = (c & d) | (~a&~b&c);
endmodule
