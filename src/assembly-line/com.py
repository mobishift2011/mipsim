from myhdl import always_comb, block, intbv


@block
def Add(out, in0, in1):
    """加法器"""
    @always_comb
    def _add():
        out.next = in0 + in1
    return _add


def Sub(in0, in1):
    """减法器"""
    return intbv(in0 - in1)[32:]


@block
def Mux(out, in0, in1, sel):
    """2x1多选器"""
    @always_comb
    def _mux():
        out.next = [in0, in1][sel]

    return _mux


def And(out, in1, in2):
    """与门"""
    @always_comb
    def _and():
        out.next = in1 and in2

    return _and


def Or(out, in1, in2):
    """或门"""
    @always_comb
    def _or():
        out.next = in1 or in2

    return _or
