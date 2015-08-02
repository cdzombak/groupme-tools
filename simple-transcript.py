import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime


def printTranscript(messages, outputFilename):
    """Prints a readable "transcript" from the given list of messages.

    Assumes the input list is sorted."""
    with open(outputFilename, 'wb') as outFile:
        for message in messages:
            name = message[u'name']
            time = datetime.datetime.fromtimestamp(message[u'created_at']).strftime('%Y-%m-%d %H:%M')

            # text is None for a photo message
            if message[u'text'] is not None:
                text = message[u'text']
            else:
                text = "(no text)"

            if message[u'system'] is True:
                system_padded = '(SYS) '
            else:
                system_padded = ''

            if len(message[u'favorited_by']) is not 0:
                favorites_padded = ' (' + str(len(message[u'favorited_by'])) + 'x <3)'
            else:
                favorites_padded = ''

            if message[u'picture_url'] is not None:
                pic = ' ; photo URL ' + message[u'picture_url']
            else:
                pic = ''

            line = u'{0}{1}({2}){3}: {4}{5}\n'.format(
                system_padded, name, time, favorites_padded, text, pic
            )
            outFile.write(line)


def main():
    """
    Usage: simple-transcript.py transcript-filename.json output-filename.json

    Assumes filename.json is a JSON GroupMe transcript in chronological order.

    Times displayed in local timezone.
    """

    if len(sys.argv) < 3:
        print(main.__doc__)
        sys.exit(1)

    with open(sys.argv[1]) as transcriptFile:
        transcript = json.load(transcriptFile)

    printTranscript(transcript, sys.argv[2])


if __name__ == '__main__':
    main()
    sys.exit(0)
