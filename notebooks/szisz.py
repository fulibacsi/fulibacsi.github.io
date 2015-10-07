# encoding: utf-8
# Util file for the Python101 - SzISz course 3rd class.

# ============ imports ============
import os
import string
import operator
import csv
import codecs
import random
import re
import IPython.display

#  ============ globals ============
OR = operator.or_
AND = operator.and_

# ============ functions ============

# Image print
def print_image(source, _type='img', width=None, height=None):
    """Display an image. (IPython notebook exclusive!)
    Arguments:
        source: image URI.
        _type: the type of the image. available values:
            - net: URL
            - svg: svg image
            - img: standard image
        _width: display width
        _height: display height
    """
    if _type == 'net':
        IPython.display.display(
            IPython.display.Image(url=source, width=width, height=height)
        )
    elif _type == 'img':
        IPython.display.display(
            IPython.display.Image(filename=source, width=width, height=height)
        )
    elif _type == 'svg':
        IPython.display.display(
            IPython.display.SVG(source, width, height)
        )

# CSV reader
def import_from_csv(filename):
    """Returns the rows from the specified csv file.
    Arguments:
        filename: the file to read.
    Returns:
        List of the rows (where the values in the row are in a list).
    """
    data = []
    with open(filename, 'r') as csvfile:
        CSV = csv.reader(csvfile, dialect='excel')
        for row in CSV:
            data.append(row)
    return data

# CSV writer
def export_to_csv(filename, data):
    """Writes the data lines into a csv file.
    Arguments:
        filename: the file to write the data to.
        data: the data to write.
    Returns:
        -
    """
    if '.csv' not in filename:
        filename += '.csv'
    with open(filename, 'w') as csvfile:
        CSV = csv.writer(csvfile, dialect='excel')
        for row in data:
            CSV.writerow(row)

# file listing
def list_files(target_dir=''):
    """Collect the filenames from the specified directory.
    Argument:
        target_dir: subdirectory name. default: working directory.
    Returns:
        Filenames from the specified directory as a list."""
    if len(target_dir):
        if not target_dir[0] == '/':
            target_dir = '/' + target_dir
    return [_file
        for _file in os.listdir('.' + target_dir)
        if os.path.isfile('.' + target_dir + '/' + _file)
    ]

# fake download function
def download(_name='super_series', _seasons=7, _episodes=24, _mismatch=False):
    """Download the specified series into a directory.
    One should wear sunglass to avoid injuries caused by this awesome function!

    Arguments:
        _name: name of the series. default: 'super_series'
        _seasons: the number of seasons. default: 7
        _episodes: the number of episodes in a season. default: 24
        _mismatch: does the subtitle names matches?
    Returns:
        Log text.
    """
    seasons = xrange(1, _seasons+1)
    episodes = xrange(1, _episodes+1)
    movie_ext = 'avi'
    subtitle_ext = 'srt'
    subdir = './' + _name
    obfuscation = ['hdtv.xvid', 'hdtv.fov', '720p-avg', 'x264.eng', 'BDRip']
    separators = ['.', ' ', '_', ' - ', '-']
    possible_items = [{'season': s, 'episode': e, 'extension': x}
                      for x in [movie_ext, subtitle_ext]
                      for e in episodes
                      for s in seasons]
    if _mismatch:
        filename = '{filename}{sep1}S{season}E{episode}{sep2}{obfuscation}.{extension}'
    else:
        filename = '{filename}.S{season}E{episode}.{extension}'

    try:
        os.mkdir(subdir)
    except Exception:
        pass

    try:
        for item in possible_items:
            if _mismatch:
                path = subdir + '/' + filename.format(
                    filename=_name,
                    season=str(item['season']).zfill(2),
                    episode=str(item['episode']).zfill(2),
                    sep1=random.choice(separators),
                    sep2=random.choice(separators),
                    obfuscation=random.choice(obfuscation),
                    extension=item['extension']
                )
                if random.randint(0,1):
                    path = path.lower()
                elif random.randint(0,1):
                    path = path.upper()
            else:
                path = subdir + '/' + filename.format(
                    filename=_name,
                    season=str(item['season']).zfill(2),
                    episode=str(item['episode']).zfill(2),
                    extension=item['extension']
                )
            # file creation
            open(path, 'w').write(path)
    except Exception as e:
        return 'Creation process failed, ERROR:', e.message
    else:
        return 'Creation successful.'

# rename erroneous subtitle
def rename_subtitle(original, new, target_dir):
    """Renames the specified file to a new name.
    Arguments:
        original: original filename
        new: new filename
    Returns:
        -
    """
    if len(target_dir):
        if not target_dir[0] == '/':
            target_dir = '/' + target_dir
        if not target_dir[-1] == '/':
            target_dir = target_dir + '/'
    if original in list_files(target_dir):
        os.rename('.' + target_dir + original, '.' + target_dir + new)

def find_episode_number(filename):
    """Finds the seasons and episode numbers.
    Arguments:
        filename: the filename containing the seasons and episode numbers
    Returns:
        The seasons-episode numbers (sXXeYY X in series numbers, Y in episode
        numbers) or None if the number was not found.
    """
    pattern = re.compile(r'(\S+)[\.|\ |\ -\ |_|\-]'
                          '(?P<number>[S|s][0-9]+[E|e][0-9]+)')
    match = re.search(pattern, filename)
    if match:
        return match.group('number')
    else:
        return None

def encrypt(text, strength=4, level=1):
    """"Encrypt" a text by inserting random character [strength] times
    (level=1), and by  sliding the letters by [strength] positions (level=2),
    eg. the input letter 'a' becomes 'c' if strength equals 2.

    Parameters:
    -----------
    text: string
        Input text to be transformed.
    strength: int
        Intensity parameter. It will be used to determine the number of
        distortion characters and the sliding intensity.
    level: [1, 2]
        Level of encription:
            1) Only distortion characters inserted
            2) Beside distortion characters, the characters of the input
               strings also slides.

    Returns:
    --------
    encrypted: string
        The encrypted text.

    """
    abc = string.ascii_letters
    distortion = xrange(strength - 1)
    if level == 1:
        encrypted = [
            char +
            ''.join([random.choice(abc) for i in distortion])
            for char in text
        ]
    elif level == 2:
        encrypted = [
            chr(ord(char)+strength) +
            ''.join([random.choice(abc) for i in distortion])
            for char in text
        ]

    return ''.join(encrypted)

    