from myhdl import always, block, intbv, instances

i_mem = [intbv(0)[8:], intbv(1)[8:], intbv(2)[8:], intbv(3)[8:],
         intbv(4)[8:], intbv(5)[8:], intbv(6)[8:], intbv(7)[8:]]

d_mem = []


@block
def IRAM(clk, out, address):
    """指令内存, 根据address地址获得内存指令并由out输出"""
    @always(clk.posedge)
    def access():
        addr = address.val
        byte_arr = i_mem[addr: addr+4]
        val = intbv(0)[32:]
        val[32:24] = byte_arr[0]
        val[24:16] = byte_arr[1]
        val[16:8] = byte_arr[2]
        val[8:0] = byte_arr[3]
        out.next = val

        print(f'fetch instruction: {bin(out.next)}')

    return access


@block
def DRAM():
    return instances
