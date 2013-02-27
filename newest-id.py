import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime


def main():
    """Usage: newest-id.py filename.json

Assumes filename.json is a JSON GroupMe transcript in chronological order.
    """

    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)

    transcriptFile = open(sys.argv[1])
    transcript = json.load(transcriptFile)
    transcriptFile.close()

    print(transcript[-1][u'id'])


if __name__ == '__main__':
    main()
    sys.exit(0)
