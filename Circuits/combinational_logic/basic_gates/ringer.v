 module top_module (
    input ring,
    input vibrate_mode,
    output ringer,       // Make sound
    output motor         // Vibrate
);
    //assign {ringer, motor} = {ring | ~vibrate_mode,  ~ring | vibrate_mode};
//    assign {ringer, motor} ={~(~ring & vibrate_mode), ~( ring & ~vibrate_mode)};
    assign {ringer, motor} = {~vibrate_mode & ring,vibrate_mode & ring };

endmodule
