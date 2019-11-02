from myhdl import always, always_comb, block, intbv

i_mem = [
    intbv(140)[8:], intbv(68)[8:], intbv(0)[8:], intbv(4)[8:],  # lw $4, 4($2)
    intbv(172)[8:], intbv(66)[8:], intbv(0)[8:], intbv(8)[8:]  # sw $2, 8($2)
]


@block
def IRAM(clk, out, address):
    """指令内存, 根据address地址获得内存指令并由out输出"""
    @always(clk.posedge)
    def access():
        addr = address
        byte_arr = i_mem[addr: addr+4]
        val = intbv(0)[32:]
        val[32:24] = byte_arr[0]
        val[24:16] = byte_arr[1]
        val[16:8] = byte_arr[2]
        val[8:0] = byte_arr[3]
        out.next = val

        print(f'fetch instruction: {bin(out.next)}')

    return access


def parse_code(code):
    return []


def set_instruction_mem(code):
    results = parse_code(code)
    i_mem.append(intbv(results[0][32:]))
    i_mem.append(intbv(results[1][32:]))
    i_mem.append(intbv(results[2][32:]))
    i_mem.append(intbv(results[3][32:]))


d_mem = [intbv(0)[8:]]*256  # 模拟256B大小的数据内存块
d_mem[0:4] = [intbv(1)[8:]] * 4
d_mem[4:8] = [intbv(2)[8:]] * 4
d_mem[8:12] = [intbv(3)[8:]] * 4


@block
def DRAM(clk, out_data, alu_out, in_data,  MemWrite, MemRead, MemtoReg):
    @always_comb
    def read():
        print('ALU OUT:', alu_out)
        if MemtoReg:
            if MemRead:
                addr = alu_out
                data = intbv(0)[32:]
                data[32:24] = d_mem[addr]
                data[24:16] = d_mem[addr+1]
                data[16:8] = d_mem[addr+2]
                data[8:0] = d_mem[addr+3]
                out_data.next = data
        else:
            out_data.next = alu_out

    @always(clk.negedge)
    def write():
        addr = alu_out
        d_mem[addr] = in_data[32:24]
        d_mem[addr+1] = in_data[24:16]
        d_mem[addr+2] = in_data[16:8]
        d_mem[addr+3] = in_data[8:0]

    return read, write
