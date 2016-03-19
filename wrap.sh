while true; do
    xvfb-run -a -e /dev/stdout python -u get_lyrics_from_site.py | tee log.log;
done
