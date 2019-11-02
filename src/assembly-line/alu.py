from myhdl import always_comb, block, intbv


@block
def ALU(iram_out, alu_out, read_data1, read_data2, Zero, ALUOp0, ALUOp1, ALUSrc):
    @always_comb
    def access():
        ALUControlSignal = [0, 0, 0, 0]
        # alu control signal
        if ALUOp0 == 0 and ALUOp1 == 0:
            ALUControlSignal[2] = 1
        elif ALUOp0 == 0 and ALUOp1 == 1:
            ALUControlSignal[1] = 1
            ALUControlSignal[2] = 1
        else:
            sum = iram_out[6:0]
            if sum == 0b100000:  # case 32
                ALUControlSignal[2] = 1
            elif sum == 0b100010:  # case 34
                ALUControlSignal[1] = 1
                ALUControlSignal[2] = 1
            elif sum == 0b100100:
                pass
            elif sum == 0b100101:
                ALUControlSignal[3] = 1
            elif sum == 0b101010:
                ALUControlSignal[1] = 1
                ALUControlSignal[2] = 1
                ALUControlSignal[3] = 1
            else:
                pass

        # alu out
        immi_num = iram_out[16:0]
        if ALUSrc == 0b1:
            if ALUControlSignal[1] == 0:
                alu_out.next = read_data1.val + read_data2.val
            if ALUControlSignal[1] == 1:
                alu_out.next = read_data1.val - read_data2.val
        
        if ALUSrc == 0b0:
            if ALUControlSignal[1] == 0:
                alu_out.next = read_data1.val + immi_num
            if ALUControlSignal[1] == 1:
                alu_out.next = read_data1.val - immi_num
    return access
