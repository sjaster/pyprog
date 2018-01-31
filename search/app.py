#! /usr/bin/env python3

import sys
import os
from time import time

# PDF
from PyPDF2 import PdfFileWriter, PdfFileReader
# MP3
from mutagen.easyid3 import EasyID3
# Word documents
from docx import Document


def isTextInWord(needle='', file=None):

    doc = Document(file)
    for paragraph in doc.paragraphs:
        if needle in paragraph.text:
            return True

    return False


def isTextInMp3(needle='', file=None):

    audio = EasyID3(file)
    for tag in audio:
        if needle in audio[tag][0]:
            return True

    return False


def isTextInPdf(needle='', file=None):
    pdf = PdfFileReader(open(file, 'rb'))

    for i in range(pdf.getNumPages()):
        text = pdf.getPage(i).extractText()
        if needle in text:
            return True

    return False


def isTextInFile(needle='', file=None):
    # TODO Check if file exists
    if needle is '' or file is None:
        return False

    extension = os.path.splitext(file)[1]
    extension = extension[1:]

    try:
        if extension == 'pdf':
            return isTextInPdf(needle, file)

        elif extension == 'mp3':
            return isTextInMp3(needle, file)

        elif extension == 'docx':
            return isTextInWord(needle, file)

        else:
            with open(file, mode='r') as f:
                body = f.read()
                if needle in body:
                    return True
                else:
                    return False
    except:
        return False


def main():

    directories_to_search = []
    needles = []

    args = sys.argv[1:]

    for arg in args:
        if os.path.isdir(arg):
            directories_to_search.append(
                os.path.abspath(arg))
        else:
            needles.append(arg)`

    print('Starting search... \n')
    start_time = time()

    results = []

    for current_directory in directories_to_search:
        for needle in needles:
            # The Search
            for root, dirs, files in os.walk(current_directory):
                for file in files:
                    filename = os.path.join(root, file)
                    if isTextInFile(needle=needle, file=filename):
                        results.append(filename)

    # Print results
    # root_length = len(os.path.dirname(root_directory_absolute)) + 1
    root_length = 0
    for result in results:
        print(result[root_length:])

    end_time = time()
    print('\n Found: {} files in: {}s'.format(
        len(results),
        round(end_time - start_time, 1)
    ))


try:
    main()
except KeyboardInterrupt:
    pass
