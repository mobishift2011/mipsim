from myhdl import always, always_comb, block, delay, intbv
from com import Mux

_registers = [intbv(0)[32:]] * 32


@block
def RegisterFile(clk, read_addr1, read_addr2, read_data1, read_data2, rt, rd, write_addr, write_data, immediate, RegWrite, RegDst, ALUSrc):
    mux = Mux(write_addr, rt, rd, RegDst)

    @always_comb
    def read():
        assert len(read_addr1) == 5
        assert len(read_addr2) == 5
        assert len(read_data1) == 32
        assert len(read_data2) == 32
        assert len(immediate) == 16
        assert len(write_addr) == 5

        read_data1.next = _registers[read_addr1.val]
        immediate_ext = intbv(0)[32:]
        immediate_ext[16:0] = immediate.val
        read_data2.next = _registers[read_addr2.val]

        print(f'RegWrite {RegWrite.val}')
        print(f'RegDst {RegDst.val}')
        print(f'ALUSrc {ALUSrc.val}')
        # print(f'{read_data1.next} at &{read_addr1.val}')
        # print(f'{read_data2} at &{read_addr2.val}')
        # print(f'write port &{write_addr.val}')

    @always(clk.negedge)
    def write():
        assert len(write_addr) == 5
        assert len(write_data) == 32
        if RegWrite and write_addr:
            _registers[write_addr] = write_data
            print(f'write {write_data} to register &{write_addr}')

    return mux, read, write
