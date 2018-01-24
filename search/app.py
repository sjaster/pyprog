import sys
import os
from time import time


def isTextInFile(needle='', file=None):
    # TODO Check if file exists
    if needle is '' or file is None:
        return False

    try:
        if os.path.splitext(file) is 'pdf':
            pass
        elif os.path.splitext(file) is 'mp3':
            pass
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

    root_directory = sys.argv[1]
    root_directory_absolute = os.path.abspath(root_directory)
    needle = sys.argv[2]

    print('Starting search... \n')
    start_time = time()

    results = []

    # The Search
    for root, dirs, files in os.walk(root_directory_absolute):
        for file in files:
            filename = os.path.join(root, file)
            if isTextInFile(needle=needle, file=filename):
                results.append(filename)

    # Print results
    root_length = len(os.path.dirname(root_directory_absolute)) + 1
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
