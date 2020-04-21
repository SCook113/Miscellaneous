import argparse
import os
import shutil
from functools import partial
from argparse import RawTextHelpFormatter
import pandas as pd
from pytube import Playlist, YouTube


def extract_urls(youtube_url):
    """Extracts urls for videos to be downloaded

        Parameters:
        youtube_url (str): Url of playlist or video

        Returns:
        list: list of all urls

       """
    try:
        download_items = Playlist(youtube_url)
        print('It is a playlist')
        return download_items
    except:
        print('It is a video')
        return list([youtube_url])


def make_playlist_directory(save_destination, playlist_name):
    """Creates a temo directory and a direcotry for final files

        Parameters:
        save_destination (str): Where finished files will be stored
        playlist_name (str): Name of playlist or video folder

       """
    if not os.path.exists(f'temp/{playlist_name}'):
        os.makedirs(f'temp/{playlist_name}')
        print("Directory ", playlist_name, " in /temp Created ")
    else:
        print("Directory ", playlist_name, " on /temp already exists")

    if not os.path.exists(f'{save_destination}/{playlist_name}'):
        os.mkdir(f'{save_destination}/{playlist_name}')
        print("Directory ", f'{save_destination}/{playlist_name}', " Created ")
    else:
        print("Directory ", f'{save_destination}/{playlist_name}', " already exists")


def add_index(video_name, download_number):
    """Adds the index of the download to a filename

        Parameters:
        video_name (str): name of video
        download_number: number that will be set at beginning of string

        Returns:
        str: formatted string

       """
    return str(download_number) + '_-_' + video_name


def download_playlist(save_destination, playlist_name, playlist_url, convert):
    """Downloads a playlist

        This function makes a temporary directory for downloaded files,
        checks if url is a video or a playlist,
        downloads all the audio of the video,
        moves them to the save destination and
        removes temp directory.

        Parameters:
        save_destination (str): path to where the files should be stored
        playlist_name(str): name of the video or playlist (folder will be named after this)
        playlist_url(str): url of the playlist/video
        convert(bool): flag if video(s) should be converted to mp3

       """
    print(f'Playlist name: {playlist_name}')
    make_playlist_directory(save_destination, playlist_name)
    playlist = extract_urls(playlist_url)
    video_name = 0
    data_format = 1
    print('Number of videos in playlist: %s' % len(playlist))

    for index, video in zip(range(1, len(playlist) + 1), playlist):
        vid = YouTube(video)
        print(f'{index}/{len(playlist)}', vid.title)
        # Add index to filename
        file_name_form = add_index(vid.title, index)

        # TODO Check if file has been downloaded before
        # only download if it doesn't exist

        # Download Audio
        vid.streams.get_audio_only().download(f'temp/{playlist_name}')

        # Try to rename files
        for fname in os.listdir(f'temp/{playlist_name}'):
            if vid.title == fname.split('.')[video_name]:
                shutil.move(f'temp/{playlist_name}/{fname}',
                            f'temp/{playlist_name}/{".".join([file_name_form, fname.split(".")[data_format]])}')
        
        if convert is True:
            # Convert to mp3
            os.system(f'audioconvert convert temp/{playlist_name} {save_destination}/{playlist_name} -o .mp3')
        else:
            # Move files
            for fname in os.listdir(f'temp/{playlist_name}'):
                shutil.move(f'temp/{playlist_name}/{fname}',
                                f'{save_destination}/{playlist_name}/{fname}')

        # Remove temp files
        shutil.rmtree(f'temp/{playlist_name}')

    # Remove temp files
    shutil.rmtree(f'temp')


parser = argparse.ArgumentParser(description='test', formatter_class=RawTextHelpFormatter)
parser.add_argument('--d', type=str, default='../../Desktop/EINGANG',
                    help='Folder path where files should be stored in (example: ./myfolder/mysubfolder)')
parser.add_argument('--c', type=str, default=True,
                    help='Flag if audio should be converted to mp3 (True = Yes, False = No, Default value is True)')
parser.add_argument('--pfile', type=str, default='to_download.txt',
                    help='The path to the file in which the playlist urls are stored. For every line the file should be of the format:\n<playlist name>,<url>\nRemember: Don\'t use spaces in the playlist name!!!')
args = parser.parse_args()

save_destination = args.d
convert = args.c
playlist_file = args.pfile

# Make a partial function
# No special reason for this, I just wanted to practice partials
download_playlist_pl = partial(download_playlist, save_destination)

# Read in file with playlist urls
list_of_playlists = pd.read_csv(playlist_file, names=['name', 'url'])

# Iteratively save playlists
for index, row in list_of_playlists.iterrows():
    # Download
    download_playlist_pl(row['name'], row['url'], convert)
    print('Done', end='\n\n')
