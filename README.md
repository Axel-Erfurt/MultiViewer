# MultiViewer
Viewer for thunar in xfce

I wrote this mainly for Thunar to have a preview function for different files.

Create a custom action with the name "Preview" and the command:

change /Path_to/MultiViewer to your path

```
sh -c "cd /Path_to/MultiViewer && python3 ./MultiViewer.py %f"
```

Files that can be displayed

- csv ["csv", "tsv"] # tab delimited
- video ["mp4", "flv", "mpg", "mpeg", "m4v", "mov", "vob", "mkv"]
- audio ["mp3", "m4a", "ogg", "flac", "wav", "aif", "aiff"]
- text ["txt", "rtf", "m3u", "m3u8", "pls", "py", "sh"]
- html ["html", "htm"]
- pdf ["pdf"]
- image ["png", "jpg", "eps", "gif", "bmp", "tiff", "tif", "jpeg", "svg"]
- odf ["odt", "doc", "docx"]
