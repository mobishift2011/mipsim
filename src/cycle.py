# -*-coding: utf-8-*-
from myhdl import always, always_comb, block, delay, instance, instances, intbv, Signal
from mem import IRAM
from com import Add, Mux

CLK_t = 200  # 一个时钟周期时长
CYCLE_c = 2  # 执行的时钟周期数


@block
def Clk():
    clk = Signal(intbv(0))

    @always(delay(100))
    def drive_clk():
        clk.next = not clk

    return drive_clk


@block
def PC(clk, address):
    din = Signal(0)

    @always(clk.posedge)
    def count():
        address.next = Add(address, 4)

    return count


@block
def ControlUnit(clk, din):
    @always(clk.posedge)
    def decode():
        op = din[32:26]
        if op == 0b0:
            pass
        elif op == 0b1:
            pass

    return decode


@block
def SingleCycle(period):
    """执行单周期操作，时钟周期period"""
    clk = Signal(intbv(0))  # 时钟信号
    address = Signal(intbv(0)[32:])
    imem_out = Signal(intbv(0)[32:])
    pc = PC(clk, address)  # PC寄存器
    imem = IRAM(clk, imem_out, address)
    cu = ControlUnit(imem_out)

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
