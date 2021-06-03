# MultiViewer
Viewer for thunar in xfce

### Requirements

- python >= 3.6
- PyQt5

I wrote this mainly for Thunar to have a preview function for different files.

Extract pdfjs.tar.gz to the MultiViewer folder.

Create a custom action with the name "Preview" and the command:

change /Path_to/MultiViewer to your path

```
sh -c "cd /Path_to/MultiViewer && python3 ./MultiViewer.py %f"
```
Then you can right-click "Preview" in thunar

Files that can be displayed

- csv ["csv", "tsv"] # tab delimited
- video ["mp4", "flv", "mpg", "mpeg", "m4v", "mov", "vob", "mkv"]
- audio ["mp3", "m4a", "ogg", "flac", "wav", "aif", "aiff"]
- text ["txt", "m3u", "m3u8", "pls", "py", "sh"]
- html ["html", "htm"]
- pdf ["pdf"]
- image ["png", "jpg", "eps", "gif", "bmp", "tiff", "tif", "jpeg", "svg"]
- odf ["odt", "doc", "docx"]

You can use it without thunar from command line

Example:

```
cd /Path_to/MultiViewer && python3 ./MultiViewer.py myfile.png
```
