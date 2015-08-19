#!/usr/bin/env python2
"""
Module to translate JSON transcript into a pretty HTML output.

This module actually should create a folder that contains an index.html as well
as all the necessary images for the transcript to be rendered in browser
completely offline.
"""

from UserDict import UserDict
from inspect import cleandoc
import json
import requests
import datetime
import os.path
import sys
import shutil

_HTML_HEADER = """<!doctype html>\n'
<html>\n<head>
<meta charset="UTF-8">
<title>GroupMe Transcript</title>
<link rel="stylesheet" type="text/css" href="groupme.css">
<script src="http://cdn.jsdelivr.net/emojione/1.5.0/lib/js/emojione.min.js"></script>
<link rel="stylesheet" href="http://cdn.jsdelivr.net/emojione/1.5.0/assets/css/emojione.min.css"/>
<script src="groupme.js"></script>
</head>\n<body>
<div class="container">
<h1>GroupMe Transcript</h1>
<div class="chat">
"""

_HTML_FOOTER = """</div>
</div>
</body>
</html>
"""


class ImageCache(UserDict):
    """Maps image URLs to local filenames."""

    def __init__(self, folder, initialdata={}):
        UserDict.__init__(self, initialdata)
        self._folder = folder

    def _save_image(self, url):
        # Full disclosure, largely adapted from this SO answer:
        # http://stackoverflow.com/a/16696317
        local_file = url.split('/')[-1]
        local = os.path.join(self._folder, local_file)
        if os.path.exists(local):
            return local_file
        print 'Downloading image.'
        resp = requests.get(url, stream=True)
        with open(local, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return local_file

    def __getitem__(self, key):
        try:
            UserDict.__getitem__(self, key)
        except KeyError:
            local = self._save_image(key)
            self[key] = local
            return local


def write_html_transcript(messages, outfile, imgcache):

    for i, message in enumerate(messages):
        # Get variables
        name = message[u'name']
        time_obj = datetime.datetime.fromtimestamp(message[u'created_at'])
        time_str = time_obj.strftime('%Y-%m-%d %H:%M')
        text = message[u'text']
        if text is None:
            text = u''
        system = message[u'system']
        faves = message[u'favorited_by']
        nlikes = faves if faves == 0 else len(faves)
        pic = message[u'picture_url']


        # Open div
        outfile.write('<div class="message-container')
        if system:
            outfile.write(' system')
        outfile.write('">')

        # Author
        outfile.write('<div class="author">')
        outfile.write(name.encode('utf-8'))
        outfile.write('</div>')

        # Message span
        outfile.write('<div class="message"><span class="message-span" title="%s">' % time_str)
        outfile.write(text.encode('utf-8'))
        outfile.write('</span></div>')

        # Likes
        if nlikes > 0:
            outfile.write('<div class="likes">')
            outfile.write("<img class='emojione' src='http://cdn.jsdelivr.net/emojione/assets/png/2764.png'>x</img>")
            outfile.write('<span class="likes-count">%d</span>' % nlikes)
            outfile.write('</div>')

        # Image
        if pic:
            local = imgcache[pic]
            outfile.write('<img src="' + local + '" class="picture-message">')

        # Close div
        outfile.write('</div>\n')

        print '%04d/%04d messages processed' % (i, len(messages))


def write_html(folder, messages, emoji=True):
    imgcache = ImageCache(folder)
    index_fn = os.path.join(folder, 'index.html')
    shutil.copyfile('assets/groupme.css', os.path.join(folder, 'groupme.css'))
    shutil.copyfile('assets/groupme.js', os.path.join(folder, 'groupme.js'))
    with open(index_fn, 'w') as f:
        f.write(_HTML_HEADER)
        write_html_transcript(messages, f, imgcache)
        f.write(_HTML_FOOTER)


def main():
    """
    Usage: html-transcript.py filename.json html-output-folder

    Takes a JSON GroupMe transcript and writes a mostly offline HTML version of
    your transcript.  Downloads all images sent over GroupMe, and uses a
    Javascript library + CDN to render all of the Emoji.  GroupMe-specific
    emoji will end up unrecognizable.
    """
    if len(sys.argv) < 3:
        print cleandoc(main.__doc__)
        sys.exit(1)

    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    trans_file = open(sys.argv[1])
    transcript = json.load(trans_file)
    trans_file.close()

    write_html(sys.argv[2], transcript)


if __name__ == '__main__':
    main()
