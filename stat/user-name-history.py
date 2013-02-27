import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime


def main():
    """Usage: user-name-history.py filename.json

Print a list of user IDs and their name history within
the group.

Assumes filename.json is a JSON GroupMe transcript.
    """

    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)

    transcriptFile = open(sys.argv[1])
    transcript = json.load(transcriptFile)
    transcriptFile.close()

    names = {}

    for message in transcript:
        name = message[u'name']
        id = message[u'user_id']

        if id not in names:
            names[id] = [name]
        else:
            if name not in names[id] and name != 'GroupMe':
                names[id].append(name)

    for id, nameList in names.items():
        nameHistory = ', '.join(nameList)
        print(id + ': ' + nameHistory)


if __name__ == '__main__':
    main()
    sys.exit(0)
