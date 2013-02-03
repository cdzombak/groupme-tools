Some things which are easy to calculate.

First, run simple-transcript.py and store it to a text file `transcript.txt`.

(Someone with better unix-fu with `awk`/`grep` can probably do cooler things than I.)

# Group inception

`head -n 1 transcript.txt`, and read the date from that post.

# Total messages

`wc -l transcript.txt`

# User name changes

`cat transcript.txt | grep "(SYS)" | grep "changed name to"` shows a history of name changes.

Pipe that through `| wc -l` for a count of user name changes.

See `user-name-history.py` for more user name fun.

# Group name changes

`cat transcript.txt | grep "(SYS)" | grep "changed the group's name"` shows a history of group name changes.

Again, pipe through `| wc -l` for a count of group name changes.

# Avatar changes

`cat transcript.txt | grep "(SYS)" | grep "changed the group's avatar"` shows a history of group avatar changes.

Unfortunately, I can't figure out how to get the actual avatars, but we can tell when they happened and who did it.

Again, pipe through `| wc -l` for a count of changes.

# Photos posted

`cat transcript.txt | grep "; photo URL"` for a list of posts with photos. Pipe through `| wc -l` for a count of photos posted.

## First photo posted

`cat transcript.txt | grep "; photo URL" | head -n 1`

# Fucks given

`cat transcript.txt | grep fuck | wc -l`
