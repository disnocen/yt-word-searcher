#!/bin/bash
dirname=$(cat .dirname)
for i in subs/$dirname/*srt;
do
    if [ -f "$i\_searched.txt" ]; then
        rm  -f "$i\_searched.txt" 
    fi
    cat $i | grep -i  "$1" >> $i\_searched.txt
    # cat $i | grep -i -A15 -B15 "$1" >> $i\_searched.txt
done
