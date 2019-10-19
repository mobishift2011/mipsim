from myhdl import always_comb, block, intbv


def Add(in0, in1):
    """加法器"""
    return intbv(in0 + in1)[32:]


def Mux(in0, in1, sel):
    """2x1多选器"""
    return [in0, in1][sel]


def And(in1, in2):
    """与门"""
    return in1 and in2


def Or(in1, in2):
    """或门"""
    return in1 or in2
