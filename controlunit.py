from myhdl import always_comb, block, intbv


@block
def ControlUnit(iram_out, RegDst, Branch, MemRead, MemtoReg, ALUOp1, ALUOp0, MemWrite, ALUSrc, RegWrite, read_addr1, read_addr2, rt, rd, immediate):
    @always_comb
    def decode():
        opcode = iram_out.val[32:26]

        if opcode == 0b000000:
            tmp = [intbv(1)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[1:], intbv(1)[
                1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[1:], intbv(1)[1:]]
        elif opcode == 0b100011:
            tmp = [intbv(0)[1:], intbv(0)[1:], intbv(1)[1:], intbv(1)[1:], intbv(0)[
                1:], intbv(0)[1:], intbv(0)[1:], intbv(1)[1:], intbv(1)[1:]]
        elif opcode == 0b101011:
            tmp = [intbv(0)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[
                1:], intbv(0)[1:], intbv(1)[1:], intbv(1)[1:], intbv(0)[1:]]
        elif opcode == 0b000100:
            tmp = [intbv(0)[1:], intbv(1)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[
                1:], intbv(1)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[1:]]
        else:
            tmp = [intbv(0)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[
                1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[1:], intbv(0)[1:]]
        RegDst.next, Branch.next, MemRead.next, MemtoReg.next, ALUOp0.next, ALUOp1.next, MemWrite.next, ALUSrc.next, RegWrite.next = tmp

        # 分配总线信号
        read_addr1.next = iram_out[26:21]
        read_addr2.next = iram_out[21: 16]
        rt.next = iram_out[21: 16]
        rd.next = iram_out[16: 11]
        immediate = iram_out[16:0]

    return decode
