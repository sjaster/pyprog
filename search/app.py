__version__ = '0.1'

from sys import argv
from argparse import ArgumentParser
from time import time
import os
import mmap

parser = ArgumentParser(prog='pySyrch')
parser.add_argument('-s', '--search', nargs=1, dest='root',  metavar='<folder-to-search>', required=True,
                    help='Directory in which to search')
parser.add_argument('-t', '--for', required=True, metavar='myText', dest='needle',
                    help='What you are searching for')


def inFileMemoryEfficient(text, file):
    try:
        with open(file, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
                if s.find(text.encode()) != -1:
                    return True
                else:
                    return False
    except:
        return False


def inFile(text, file):
    try:
        with open(file, 'rb') as f:
            if text.encode() in f.read():
                return True
            else:
                return False
    except:
        return False


def search(dir, text):

    print('Searching...\n')

    results = []
    root_len = len(dir.split(os.sep))
    start_time = time()

    for root, dirs, files in os.walk(dir):

        for file in files:
            path = os.path.join(root, file)
            if inFile(text, os.path.abspath(path)):
                results.append((root, file))

    for result in results:
        path = result[0].split(os.sep)
        print((len(path) - root_len) * '---', result[1])
    print('\nDone in: {}s'.format(round(time() - start_time, 1)))


def init():
    opt = parser.parse_args(argv[1:])

    root = os.path.abspath(opt.root[0])

    if not os.path.isdir(root):
        raise NotADirectoryError('{}'.format(root))

    search(root, opt.needle)


init()
