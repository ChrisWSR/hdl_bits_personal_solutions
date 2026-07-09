module top_module(
    input clk,
    input reset,
    input  ena,
    output reg pm,
    output reg [7:0] hh,
    output reg [7:0] mm,
    output reg  [7:0] ss); 

    // seconds logic
    always @(posedge  clk) begin
        if (reset) begin
            ss <= 8'h00;
        end else if (ena) begin
            if (ss == 8'h59)begin
            	ss <= 8'h00;
        end else if (ss[3:0] == 4'd9) begin
            ss[3:0] <= 4'd0;
            ss[7:4] <= ss[7:4] + 4'd1;
        end else begin
            ss[3:0] <= ss[3:0] + 4'd1;
        end
    end
    end 
    // minutes logic
        always @(posedge  clk) begin
        if (reset) begin
            mm <= 8'h00;
        end else if (ena && (ss == 8'h59)) begin
            if (mm == 8'h59)begin
            	mm <= 8'h00;
        end else if (mm[3:0] == 4'd9) begin
            mm[3:0] <= 4'd0;
            mm[7:4] <= mm[7:4] + 4'd1;
        end else begin
            mm[3:0] <= mm[3:0] + 4'd1;
       		end
    	end
    end
    
    // hours logic
    always @(posedge  clk) begin
        if (reset) begin
            hh <= 8'h12; // restarts at 12 pm 
        end else if (ena && (ss == 8'h59) && (mm==8'h59)) begin
            if (hh == 8'h12) begin
            	hh <= 8'h01; //restarts with  1 before 12
        end else if (hh[3:0] == 4'd9) begin
            hh[3:0] <= 4'd0;
            hh[7:4] <= hh[7:4] + 4'd1;
        end else begin
            hh[3:0] <= hh[3:0] + 4'd1;
       		end
    	end
    end
    // PM AM indictator  logic
    always @(posedge clk)begin
        if (reset) begin
            pm <= 1'b0;
        end else if(ena && (ss == 8'h59) && (mm == 8'h59) && (hh == 8'h11)) begin
            pm <= ~pm;
        end
    end 
endmodule
