# -*-coding: utf-8-*-
from myhdl import always, always_comb, block, delay, instance, instances, intbv, Signal
from mem import IRAM, DRAM, d_mem
from controlunit import ControlUnit
from registerfile import RegisterFile
from alu import ALU
from com import Add, Mux, Sub

CLK_t = 200  # 一个时钟周期时长
CYCLE_c = 2  # 执行的时钟周期数


@block
def PC(clk, address):
    @always(clk.posedge)
    def count():
        address.next = address + 4

    return count


def output_result(alu_out, RegDst, ALUSrc, PCSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, ALUOp1, ALUOp0, Zero):
    print(f'RegDst: {RegDst}')
    print(f"ALUSrc: {ALUSrc}")
    print(f"PCSrc: {PCSrc}")
    print(f"MemtoReg: {MemtoReg}")
    print(f"RegWrite: {RegWrite}")
    print(f"MemRead: {MemRead}")
    print(f"MemWrite: {MemWrite}")
    print(f"Branch: {Branch}")
    print(f"ALUOp1: {ALUOp1}")
    print(f"ALUOp0: {ALUOp0}")
    print(f"Zero: {Zero}")
    print("dram:", d_mem[0:12])


@block
def SingleCycle(period):
    """执行单周期操作，时钟周期period"""
    clk = Signal(intbv(0))  # 时钟信号

    # cu控制信号
    RegDst = Signal(intbv(0)[1:])   # 目标寄存器地址rt还是rd eg. add, sw
    ALUSrc = Signal(intbv(0)[1:])   # 第二个操作数来自寄存器还是立即数 eg. add, addi
    PCSrc = Signal(intbv(0)[1:])    # PC 由 PC + 4 还是分支信号 eg.beq
    MemtoReg = Signal(intbv(0)[1:])  # 内存写入寄存器 eg. lw
    RegWrite = Signal(intbv(0)[1:])  # 寄存器写入 eg. add
    MemRead = Signal(intbv(0)[1:])  # 内存读 eg. lw
    MemWrite = Signal(intbv(0)[1:])  # 内存写 eg. sw
    Branch = Signal(intbv(0)[1:])   # 分支 eg. beq, j
    ALUOp1 = Signal(intbv(0)[1:])   # ALU控制 eg. 加，减，比较
    ALUOp0 = Signal(intbv(0)[1:])   # 与ALUOp1联合使用
    Zero = Signal(intbv(0)[1:])     # 零标志分支 eg. beq

    # 其他总线
    address = Signal(intbv(0)[32:])
    iram_out = Signal(intbv(0)[32:])
    read_addr1 = Signal(intbv(0)[5:])
    read_addr2 = Signal(intbv(0)[5:])
    write_addr = Signal(intbv(0)[5:])
    rt = Signal(intbv(0)[5:])
    rd = Signal(intbv(0)[5:])
    write_data = Signal(intbv(0)[32:])
    read_data1 = Signal(intbv(0)[32:])
    read_data2 = Signal(intbv(0)[32:])
    immediate = Signal(intbv(0)[16:])
    alu_out = Signal(intbv(0)[32:])

    # 状态单元
    pc = PC(clk, address)                # PC寄存器
    iram = IRAM(clk, iram_out, address)  # 指令内存
    rf = RegisterFile(clk, read_addr1, read_addr2, read_data1, read_data2,
                      rt, rd, write_addr, write_data, immediate, RegWrite, RegDst, ALUSrc)
    dram = DRAM(clk, write_data, alu_out, read_data2,
                MemWrite, MemRead, MemtoReg)

    # 组合逻辑单元
    cu = ControlUnit(iram_out, RegDst, Branch, MemRead, MemtoReg,
                     ALUOp1, ALUOp0, MemWrite, ALUSrc, RegWrite, read_addr1, read_addr2, rt, rd, immediate)  # 控制单元

    alu = ALU(iram_out, alu_out, read_data1,
              read_data2, Zero, ALUOp0, ALUOp1, ALUSrc)

    @instance
    def drive_clk():
        """
        每半个周期触发一次时钟边沿改变，
        仅当上升沿时为一个周期开始
        """
        half_clk = int(period / 2)
        count = 0
        while True:
            yield delay(half_clk)
            clk.next = 1
            count += 1
            print(
                f"========================cycle {count} start========================")
            yield delay(half_clk)
            output_result(alu_out, RegDst, ALUSrc, PCSrc, MemtoReg,
                          RegWrite, MemRead, MemWrite, Branch, ALUOp1, ALUOp0, Zero,)
            clk.next = 0

    return instances()


inst = SingleCycle(CLK_t)
inst.run_sim(CLK_t * CYCLE_c)
