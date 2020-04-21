# Download Youtube Audio Files

Sometimes I need to be able to listen to music while being offline, so this is a script I wrote
for myself that downloads audio from either youtube videos or entire youtube playlists and 
converts them to mp3 for me.

The script takes a text or csv file that should contain a list of the names of the videos / playlist and the corresponding urls
in the format:

\<playlist name>,\<playlist url>

Don't use spaces in the playlist names when creating this file.

The audio files will be downloaded to a temporary folder and then either moved to a destination folder directly or
converted to mp3 before doing so. I they are not converted the downloaded files will be in mp4 format.

Please review the script for the libraries you need in order to run this.

Run "playlist_download.py -h" in order to see available options.
You may also need to edit source code since the script is mainly tailored for my use only.