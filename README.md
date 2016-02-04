# groupme-tools

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

Tools to fetch the complete history of a GroupMe group chat and analyze it.

`groupme-fetch.py` allows you to grab the entire transcript for one of your groups and save it as JSON for backup and analysis. It is documented; run it with `--help` for help. It also allows you to fetch recent updates in the group to keep your JSON file up to date.

`simple-transcript.py` processes a JSON file into a human-readable text transcript.

The files in the `stat` folder are self-explanatory; they allow for learning interesting things about the transcript's content and the group's history.

## Finding your access token

**nb. there are better ways to do this now; see [GroupMe API docs](https://dev.groupme.com/docs/v3).**

Log into [GroupMe's web interface](https://web.groupme.com/groups) and use Chrome or Safari's inspector to monitor the network requests when you load one of your groups.

You'll notice a GET request to an endpoint `https://v2.groupme.com/groups/GROUP_ID/messages`.

One of the headers sent with that request, `X-Access-Token`, is your access token.

## Finding your group ID

**nb. there are better ways to do this now; see [GroupMe API docs](https://dev.groupme.com/docs/v3).**

Again, in GroupMe's web interface, the group ID is the numeric ID included in the group's URL (`https://web.groupme.com/groups/GROUP_ID`).

## Requirements/Dependencies/Python

This was written and tested on Python 2.7, because I didn't want to waste time getting my [Homebrew](https://github.com/mxcl/homebrew/wiki/Homebrew-and-Python) installation to install things for Python 3. I suspect this script will break if you run it with Python 3, because Unicode.

The only other dependency is [Requests](http://docs.python-requests.org/en/latest/). `pip install requests`. At the time of writing, the current version was 1.1.0.

## Emoji

`groupme-fetch.py` will store emoji and other non-ASCII characters in the transcript JSON fine, as expected.

## Stress testing/performance

These tools have been tested with a transcript containing ~16,000 messages on a 1.7GHz/4GB Macbook Air. It works fine.

## Keep your transcript up to date

After your initial fetch with `groupme-fetch.py`, optionally using the `oldest` option to fetch older history. You should have a complete transcript up to the last time you fetched. Then...

Note the `oldest` or `newest` parameters are message IDs from your transcript JSON file.

`python groupme-fetch.py GROUPID ACCESSTOKEN newest $(python newest-id.py transcript-GROUPID.json)`
