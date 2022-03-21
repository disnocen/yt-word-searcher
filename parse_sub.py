#!/usr/local/bin python3
import sys
import webvtt


def give_times(time_string):
    (h,m,s) = time_string.split(':')
    h = float(h)
    m = float(m)
    s = float(s)
    return h*3600+m*60+s

for file in sys.argv[1:]:
    for caption in webvtt.read(file):
        cs=give_times(caption.start)
        ce=give_times(caption.end)
        if ce-cs > .99:
            textt=caption.text.split("\n")[0]
            print(f'{caption.start} ==> {caption.end}:::{textt}')
            # print(f'time elapsed is: {ce-cs} seconds ')

