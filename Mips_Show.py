import curses
import time
stdscr = curses.initscr()

c = stdscr.getstr()

for i in range(int(c)):
    stdscr.refresh()
    stdscr.addstr(0,0,"[MIPS_CMD] : lw $4, 4($2)")
    stdscr.addstr(1,0,"CLK      {}".format(i))
    stdscr.addstr(2,0,"PC       0x0000 0000")
    stdscr.addstr(3,0,"$2       0x0000 0000")
    stdscr.addstr(4,0,"$2       0x0000 0000")
    stdscr.addstr(5,0,"$2       0x0000 0000")
    stdscr.addstr(6,0,"addr0    0")
    stdscr.addstr(7,0,"addr4    4")
    stdscr.addstr(8,0,"addr8    8")
    time.sleep(1)

curses.endwin()