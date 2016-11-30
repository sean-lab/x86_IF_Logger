#!/bin/gdb -P
import gdb


'''
ex) 
> gdb -x ./extract_x86.py ./a.out
'''

print("begin execution tracing ...");

gdb.execute('set pagination off')
gdb.execute('break main')
gdb.execute('run')

with open("test.log", "w") as f:
    while (True):
        s = gdb.execute('x /i $pc', to_string=True)

        arr = s.split()

        f.write(arr[1] + "   " + s[str.index(s, ':')+1:].lstrip())
        f.flush()

        if '+' in arr[2]:
            func, inst =  arr[2][1:str.index(arr[2], '+')], arr[3]
        else:
            func, inst =  arr[2], arr[3]

        # In order to make this script to run in another architecture(i.e ARM, MIPS),
        # you might need to modify following evaluation.
        if func == 'main' and  inst == "retq":
            gdb.execute('continue')
            gdb.execute('quit')
            break

        gdb.execute('stepi', to_string=True)

print("finished execution tracing ...");
