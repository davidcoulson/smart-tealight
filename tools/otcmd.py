#!/usr/bin/env python3
"""Send OpenThread CLI commands over the XIAO's CDC ACM shell and print replies.
usage: otcmd.py PORT 'ot state' 'ot parent' ...   (a leading 'sleep N' pauses)"""
import sys, time, serial, re
port, cmds = sys.argv[1], sys.argv[2:]
s = serial.Serial(port, 115200, timeout=0.2, dsrdtr=True); s.dtr = True; s.rts = True
time.sleep(0.5); s.write(b"\r\n"); time.sleep(0.3); s.reset_input_buffer()
def run(cmd, wait=8.0):
    data = (cmd + "\r\n").encode()
    for i in range(0, len(data), 16):          # shell RX ring is 64 B: trickle it in
        s.write(data[i:i+16]); time.sleep(0.03)
    buf = b""; t0 = time.time()
    while time.time() - t0 < wait:
        c = s.read(4096)
        if c: buf += c
        if re.search(rb"(Done|Error \d+.*)\r?\n", buf) and not cmd.startswith("ot ping"):
            break
        if cmd.startswith("ot ping") and re.search(rb"packets transmitted.*\r?\n", buf):
            break
    txt = buf.decode(errors="replace")
    txt = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", txt).replace("uart:~$ ", "")  # strip ANSI + prompt redraws
    lines = [l.rstrip() for l in txt.splitlines() if l.strip() and not l.strip().startswith("uart:~$") ]
    print(f"> {cmd}"); [print("  " + l) for l in lines if l.strip() != cmd]
for c in cmds:
    if c.startswith("sleep "): time.sleep(float(c.split()[1])); continue
    run(c, wait=40 if c.startswith("ot ping") else 8)
