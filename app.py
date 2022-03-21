#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, flash, redirect
from youtubesearchpython import VideosSearch,ChannelsSearch
import sys
import subprocess
import os.path
from os import path
import shutil


def execute(cmd):
    proc = subprocess.Popen (cmd, shell=False)
    proc.communicate()
    # popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    # for stdout_line in iter(popen.stdout.readline, ""):
    #     yield stdout_line 
    # popen.stdout.close()
    # return_code = popen.wait()
    # if return_code:
    #     raise subprocess.CalledProcessError(return_code, cmd)


def create_subdirectory_name(a):
    return '_'.join(a.split())

def get_data(video_search,limit=2):
        videosSearch = VideosSearch(video_search, limit = limit)
        video_data = videosSearch.result()["result"]

        video_links = []
        video_title = []
        video_thumb = []
        video_id = []
        for i in range(len(video_data)):
            video_links.append(video_data[i]["link"])
            video_title.append(video_data[i]["title"])
            video_thumb.append(video_data[i]["thumbnails"][0]["url"])
            video_id.append(video_data[i]["id"])

        return { "video_links":video_links, "video_title":video_title, "video_id":video_id, "video_thumb":video_thumb}
            
def create_html_from_data(data, text):
        video_links = data["video_links"]
        video_title = data["video_title"]
        video_thumb = data["video_thumb"]
        video_id = data["video_id"]

        string_html=""
        for i in range(len(video_links)):
            string_html+='<div style="border:1px solid black"><div><img style="width: 270;height:151" src='+str(video_thumb[i])+'><br/><a href='+str(video_links[i])+'>'+str(video_title[i])+'</a></div>'+text[video_id[i]]+"</div><br/>\n"
        
        return string_html

# Create the application.
APP = Flask(__name__)


@APP.route('/', methods=('GET', 'POST'))
def index():
    """ Displays the index page accessible at '/'
    """
    if request.method == 'POST':
        video_search = request.form['video_search']
        word_search = request.form['word_search']
        limit = int(request.form['limit'])

        if isinstance(word_search,str):
            word_search=word_search.split()

        new_dir = create_subdirectory_name(video_search)
        f = open(".dirname", "w")
        f.write(new_dir)
        f.close()

        data = get_data(video_search, limit=limit)
        video_links = data["video_links"]


        if not (path.exists("subs/"+new_dir) and (len([name for name in os.listdir("subs/"+new_dir) if os.path.isfile(os.path.join("subs/"+new_dir, name))]) == limit)):
            #get subs of all videos
            cmd = ["sh","getter.sh"]
            for i in range(len(video_links)):
                cmd.append(video_links[i])
            execute(cmd)
        

        cmd_search = ["sh","search.sh"]
        for i in range(len(word_search)):
            cmd_search.append(word_search[i])
        execute(cmd_search)

        text = {}
        for i in range(len(data["video_id"])):
            f = open("subs/"+new_dir+"/"+data["video_id"][i]+".srt_searched.txt", "r")
            aa = f.read()
            bb = aa.split("\n")
            res_string_html = []
            for j in range(len(bb)):
                cc = bb[j].split(":::")
                if cc[0] != '':
                    yt_url= "https://www.youtube.com/watch?v=" + data["video_id"][i] 
                    dd = cc[0].split("==>")
                    ee = dd[0].split(":")
                    sec = int(ee[0])*3600+int(ee[1])*60+int(ee[2].split(".")[0])-2
                    yt_url += "&t="+str(sec)
                    res_string_html.append("<a href="+yt_url+">"+cc[0]+"</a>"+": "+cc[1])
            text[data["video_id"][i]] = "<br/>".join(res_string_html)
            f.close()



        try:
            shutil.rmtree("subs/"+new_dir)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        string_data = create_html_from_data(data,text)

        return string_data


    return render_template('index.html')


if __name__ == '__main__':
    APP.debug=True
    APP.run()
