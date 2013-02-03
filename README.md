# groupme-tools

Tools to fetch the complete history of a GroupMe group chat and analyze it.

`groupme-fetch.py` allows you to grab the entire transcript for one of your groups and save it as JSON for backup and analysis. It is documented; run it with no arguments for help. It also allows you to fetch recent updates in the group to keep your JSON file up to date.

`simple-transcript.py` processes a JSON file into a human-readable text transcript.

The files in the `stat` folder are self-explanatory; they allow for learning interesting things about the transcript's content and the group's history.

## Finding your access token

Log into [GroupMe's web interface](https://web.groupme.com/groups) and use Chrome or Safari's inspector to monitor the network requests when you load one of your groups.

You'll notice a GET request to an endpoint `https://v2.groupme.com/groups/GROUP_ID/messages`.

One of the headers sent with that request, `X-Access-Token`, is your access token.

## Stress testing/performance

These tools have been tested with a transcript containing ~16,000 messages on a 1.7GHz/4GB Macbook Air. It works fine.
