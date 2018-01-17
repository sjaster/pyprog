from pytube import YouTube
from shutil import rmtree
from subprocess import call
from re import sub
from time import time
import os
import sys

FFMPEG = None
LIST = './list.txt'
DIR_OUT = './finished'
DIR_TMP = './tmp'
FILE_IN = 'mp4'
FILE_OUT = 'mp3'


def write(s):
    print(s, end='')
    sys.stdout.flush()


def getVideoFromUrl(url):
    try:
        # Setup
        yt = YouTube(url)
        stream = yt.streams.filter(
            only_audio=True, file_extension=FILE_IN).all()[0]

        # Get info
        title = sub(r'[^0-9A-z\-\_\(\)\ \.]', '', yt.title)
        size = round(stream.filesize / 1024 / 1024, 1)
        start_time = time()

        input = '{tmp}/{file}.{ext}'.format(
            file=title, tmp=DIR_TMP, ext=FILE_IN)
        output = '{tmp}/{file}.{ext}'.format(
            file=title, tmp=DIR_OUT, ext=FILE_OUT)

        if os.path.isfile(output):
            print('Skipping {}. Already Downloaded'.format(title))
            return True

        # Downloading
        write('Downloading: {} ({}mb)... '.format(title, size))
        stream.download(output_path=DIR_TMP, filename=title)
        write('({}s) '.format(round(time() - start_time, 2)))

        # Converting
        start_time = time()
        write('Converting... ')
        call('{ffmpeg} -y -loglevel 0 -i "{input}" "{output}"'.format(
            ffmpeg=FFMPEG, input=input, output=output), shell=True)

        # Delete Video
        os.remove(input)
        print('({}s) Done.'.format(round(time() - start_time, 2)))

        return True

    except:
        print('Error getting: {}'.format(url))
        return False


def go():
    global FFMPEG

    if sys.platform == 'darwin':
        FFMPEG = './ffmpeg/macOS/ffmpeg'
    if sys.platform == 'win32':
        FFMPEG = r'.\ffmpeg\win\32\bin\ffmpeg.exe'
    if sys.platform == 'win64':
        FFMPEG = r'.\ffmpeg\win\64\bin\ffmpeg.exe'

    if FFMPEG is None:
        print('Not Comatible')
        sys.exit()

    print('Using {}'.format(FFMPEG))

    for dir in [DIR_TMP, DIR_OUT]:
        # rmtree(dir)
        if not os.path.isdir(dir):
            os.makedirs(dir)

    with open(LIST, 'r') as f:
        for l in f:
            getVideoFromUrl(l.strip())


go()
