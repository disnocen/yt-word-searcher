video_url="$@"

dirname=$(cat .dirname)
# youtube-dl  $video_url
# youtube-dl --write-auto-sub --sub-lang en --skip-download $video_url

# rename-well.sh
for i in $video_url; do
    file=$(echo "$i"| cut -d"=" -f2)
    echo "downloading subs for id $file..."
    yt-dlp -P "subs/$dirname" -o "%(id)s.%(ext)s" --write-auto-sub --sub-lang en --skip-download "$i"
    file_out=$file.srt
    python3 parse_sub.py subs/$dirname/$file.en.vtt > subs/$dirname/$file_out
    # rm subs/$dirname/$file.en.vtt
    # rm -f $file
done
