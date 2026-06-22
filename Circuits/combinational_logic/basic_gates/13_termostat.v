module top_module (
    input too_cold,
    input too_hot,
    input mode,
    input fan_on,
    output heater,
    output aircon,
    output fan
); 
    // turn on the heater when 
	assign heater = mode & too_cold;
	assign aircon = ~mode & too_hot;
	assign fan = heater | aircon | fan_on;


endmodule

// truth table
// Heater
// too_cold	too_hot	mode	heater
// 1	X	1	1
// 0	X	1	0
// X	X	0	0
// Aircon
// too_cold	too_hot	mode	aircon
// X	1	0	1
// X	0	0	0
// X	X	1	0
 
// Fan

// heater	aircon	fan_on	fan
// 1	X	X	1
// X	1	X	1
// 0	0	1	1
// 0	0	0	0
