# YTS: the Youtube Text Search

+ Goal: search for a word in 1 or more videos
+ Motivation: sometimes I want to know what a person `P` thinks about `X`. The boring thing to do is: watch videos with him. But that's tedious and time consuming. So I created YTS to search for word `X` in a list of videos from `P`.
+ How it works: 
    + given a list of youtube links, `getter.sh` dowload and parses the subs
    + use `search.sh word` to search for `word` in all subs
    + it creates a file in `subs/` called `searched.txt`: read the content of the file and use the timestamps if you really wnat to listen to that thing
