#!/usr/bin/env python3

from youtubesearchpython import VideosSearch,ChannelsSearch
import sys

limit=20
region='US'
argv =sys.argv
search_string = ""  

if argv[1] in ["channel","ch"]:
    channelsSearch = ChannelsSearch(search_string, limit = limit, region = region)
    print(channelsSearch.result())

if argv[1] in ["search","video"]:
    for i in range(2,len(argv)):
        search_string += argv[i] 


    videosSearch = VideosSearch(search_string, limit = limit)

    video_data = videosSearch.result()["result"]

    video_links = []
    for i in range(len(video_data)):
        video_links.append(video_data[i]["link"])
        

    print(video_links)

