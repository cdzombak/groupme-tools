import sys
import argparse

reload(sys)
sys.setdefaultencoding("utf-8")

import requests
import json


def onRequestError(request):
    print(request.status_code)
    print(request.headers)
    print(request.text)
    sys.exit(2)


def main():
    """
    Usage: groupme-fetch.py groupId accessToken [oldest oldestId]|[newest newestId]

    Writes out "transcript-groupId.json" with the history of the group
    in chronological order.

    If a file by that name is found, we'll go ahead and update that
    scrape depending on the options you provide. It is assumed that the
    file is in the correct format *and its messages are in chronological
    order*.

    Options for updating/continuing a scrape:

    [If neither of these options is provided, we scrape from the present
    until the job is finished (or interrupted in which case, use "oldest
    oldestId" to continue fetching the past).]

     - If "oldest oldestId" is provided, oldestId is assumed to be the ID
       of the oldest (topmost) message in the existing transcript file.
       Messages older than it will be retrieved and added at the top of
       the file, in order.

     - If "newest newestId" is provided, newestId is assumed to be the ID
       of the newest (bottom-most) message in the existing transcript file.
       Messages newer than it will be retrieved and added at the bottom
       of the file, in order.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('group')
    parser.add_argument('accessToken')
    parser.add_argument("--oldest", help="The ID of the oldest (topmost) message in the existing transcript file")
    parser.add_argument("--newest", help="The ID of the newest (bottom-most) message in the existing transcript file")
    parser.add_argument("--pages", type=int,
                        help="The number of pages to pull down (defaults to as many as the conversation has")

    args = parser.parse_args()

    group = args.group
    accessToken = args.accessToken
    beforeId = args.oldest
    stopId = args.newest
    pages = args.pages

    transcriptFileName = 'transcript-{0}.json'.format(group)
    transcript = loadTranscript(transcriptFileName)
    transcript = populateTranscript(group, accessToken, transcript, beforeId, stopId, pages)

    # sort transcript in chronological order
    transcript = sorted(transcript, key=lambda k: k[u'created_at'])

    transcriptFile = open(transcriptFileName, 'w+')
    json.dump(transcript, transcriptFile, ensure_ascii=False)
    transcriptFile.close()


def loadTranscript(transcriptFileName):
    """
    Load a transcript file by name
    """
    try:
        transcriptFile = open(transcriptFileName)
        transcript = json.load(transcriptFile)
        transcriptFile.close()
    except IOError:  # ignore FileNotFound, since that's a valid case for this tool
        transcript = []
    except ValueError:  # handle JSON parsing or empty-file error
        transcript = []
        transcriptFile.close()
    return transcript


def populateTranscript(group, accessToken, transcript, beforeId, stopId, pageLimit=None):
    complete = False
    pageCount = 0
    endpoint = 'https://v2.groupme.com/groups/' + group + '/messages'
    headers = {
        'Accept': 'application/json, text/javascript',
        'Accept-Charset': 'ISO-8859-1,utf-8',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://web.groupme.com',
        'Referer': 'https://web.groupme.com/groups/' + group,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.45 Safari/537.22',
        'X-Access-Token': accessToken
    }

    tempFileName = getTempFileName(group)
    with open(tempFileName, 'wb') as tempFile:
        while not complete:
            pageCount = pageCount + 1
            if pageLimit and pageCount > pageLimit:
                break

            print('starting on page ' + str(pageCount))

            if beforeId is not None:
                params = {'before_id': beforeId}
            else:
                params = {}
            r = requests.get(endpoint, params=params, headers=headers)

            if r.status_code is not 200:
                onRequestError(r)

            response = r.json()
            messages = response[u'response'][u'messages']

            if stopId is not None:
                messages = sorted(messages, key=lambda k: k[u'created_at'], reverse=True)
                for message in messages:
                    if message[u'id'] == stopId:
                        complete = True
                        print('Reached ID ' + stopId + "; stopping!")
                        break
                    else:
                        transcript.append(message)
            else:
                transcript.extend(messages)

            tempFile.write(json.dumps(messages))
            tempFile.write('\n')
            if len(messages) is not 20:
                complete = True
                print('Reached the end/beginning!')

            # keep working back in time
            beforeId = messages[-1][u'id']

    return transcript


def getTempFileName(group):
    return 'temp-transcript-{0}.json'.format(group)


if __name__ == '__main__':
    main()
    sys.exit(0)
