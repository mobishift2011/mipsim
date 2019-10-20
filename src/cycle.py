# -*-coding: utf-8-*-
from myhdl import always, always_comb, block, delay, instance, instances, intbv, Signal
from mem import IRAM
from com import Add, Mux

CLK_t = 200  # 一个时钟周期时长
CYCLE_c = 2  # 执行的时钟周期数


@block
def PC(clk, address):
    din = Signal(0)

    @always(clk.posedge)
    def count():
        address.next = Add(address, 4)

    return count


@block
def ControlUnit(din):
    @always_comb
    def decode():
        # socket communicate
        # decode(op)
        pass

    return decode


@block
def RegisterFile(clk):
    @always(clk.posedge)
    def access():
        pass

    return access


@block
def SingleCycle(period):
    """执行单周期操作，时钟周期period"""
    clk = Signal(intbv(0))  # 时钟信号

    # cu控制信号
    RegDst = Signal(intbv(0)[1:])  # 目标寄存器地址rt还是rd eg. add, sw
    ALUSrc = Signal(intbv(0)[1:])  # 第二个操作数来自寄存器还是立即数 eg. add, addi
    PCSrc = Signal(intbv(0)[1:])  # PC 由 PC + 4 还是分支信号 eg.beq
    MemtoReg = Signal(intbv(0)[1:])  # 内存写入寄存器 eg. lw
    RegWrite = Signal(intbv(0)[1:])  # 寄存器写入 eg. add
    MemRead = Signal(intbv(0)[1:])  # 内存读 eg. lw
    MemWrite = Signal(intbv(0)[1:])  # 内存写 eg. sw
    Branch = Signal(intbv(0)[1:])  # 分支 eg. beq, j
    ALUOp1 = Signal(intbv(0)[2:])  # ALU控制 eg. 加，减，比较
    ALUOp0 = Signal(intbv(0)[2:])  # 与ALUOp1联合使用

    # 其他总线
    address = Signal(intbv(0)[32:])
    iram_out = Signal(intbv(0)[32:])

    # 状态单元
    pc = PC(clk, address)  # PC寄存器
    iram = IRAM(clk, iram_out, address)  # 制冷内存
    # cu = ControlUnit(iram_out)
    # dram = IRAM(clk)

    @instance
    def drive_clk():
        """
        每半个周期触发一次时钟边沿改变，
        仅当上升沿时为一个周期开始
        """
        half_clk = int(period / 2)
        while True:
            yield delay(half_clk)
            clk.next = 1
            yield delay(half_clk)
            clk.next = 0

    return instances()


inst = SingleCycle(CLK_t)
inst.run_sim(CLK_t * CYCLE_c)
