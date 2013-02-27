import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime


def main():
    """Usage: posts-by-user.py filename.json

Assumes filename.json is a JSON GroupMe transcript.
    """

    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)

    transcriptFile = open(sys.argv[1])
    transcript = json.load(transcriptFile)
    transcriptFile.close()

    names = {}
    counts = {}

    for message in transcript:
        name = message[u'name']
        id = message[u'user_id']

        names[id] = name

        if id not in counts:
            counts[id] = 0
        else:
            counts[id] = counts[id] + 1

    totalMessages = len(transcript)
    print('total message count: ' + str(totalMessages))

    for id, count in counts.items():
        name = names[id]
        percentage = round(count/float(totalMessages) * 100)
        print(name + ': ' + str(count) + ' (' + str(percentage) + '%)')


if __name__ == '__main__':
    main()
    sys.exit(0)
