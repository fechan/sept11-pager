# 9/11 NYC Pager Log Dataset
This repository contains a CSV and JSON version of the all_messages pager log provided in the [9/11 pager leaks](https://911.wikileaks.org/files/index.html) released by Wikileaks in 2009. These logs contain pager messages from 3 AM EDT on September 11, 2001 to 3 AM the following day. I reccommend watching [this short YouTube documentary](https://www.youtube.com/watch?&v=inigBzDU8mw) about the 9/11 pager leaks as a primer to give this data some context.

I had to do a bit of guesswork with these field names, since I do not have a comprehensive reference and I have never used a pager myself. If you have ideas or clarification, please add your suggestion in the repo's GitHub Issues page.

**JSON users:** All fields are strings. This does not matter to CSV users.
|Field name|Format|Description|
|---|---|---|
|msg_no|number|Message number corresponding to the line it appears in the original `messages_all.txt` EXCEPT for 448358, which was separated from the mangled message 173961.|
|date|YYYY-MM-DD ([ISO 8601 Level 2](https://www.loc.gov/standards/datetime/))|Date when the message was received in. (Level 2 is for the date and time uncertainty of message 448358)|
|time|HH:MM:SS ([ISO 8601 Level 2](https://www.loc.gov/standards/datetime/))|Time when the message was received, in 24-hour format. Single digits are preceded by a 0. (Level 2 is for the date and time uncertainty of message 448358)|
|network|string|Name of the carrier network|
|capcode|number|CAP code/pager number of the recipient's pager|
|time2|HH:MM:SS AM/PM|Not sure. In 12-Hour AM/PM format. Single digits are *not* preceded by anything. Seems to be ~3 hours off of `time`, and only appears at the end of Metrocall multipart messages.|
|pocsag_mode|1, 2, or 3|Not sure. Only exists if the pager message uses the POCSAG protocol. Mutually exclusive with `function`, `mode`, and `time2`|
|pocsag_rate|1200 or 2400|POCSAG data rate, in bits per second|
|function|A, B, C, or D|Not sure. Probably corresponding to the ABCD dial on a pager.|
|mode|string|Type of message. ALPHA = alphanumeric, ST/SF NUM = numeric, TONE = beep, etc.|
|content|string|Message content|

## Message 173961 and 448358
```
2001-09-11 12:17:05 Skytel [004087318] 9:17:05 AM B ST NUM  660-665-6372 (6[1060433582] D  ALPHA  6.eing (Seal Beach) 52-880 UPDATE,TT#: (Info) 1973461, File server FIL-SC1-42 down 2:00pm 09/10 for emer.maint.affecting 400 users. Server not expected back online until 08:00 PDT 09/12.Per R.Johnson 562-982-6457 Dan(800) 278-1769
```

Message 173961 seems to be mangled in the original log. `parse.py` will fail to parse it, and looking at the original data, the line appears to be two pager messages stuck together with some information missing from the second message (message 448358). I've added a manual fix in `parse.py` called `HOTFIX_MSG_173961` that hardcodes the info for these messages.

From the original location of 448358, it's logical to assume it's happened on the same day and second as 173961, but as it's uncertain, I've used ISO 8601 Level 2 uncertainty marking for these. The network is missing, so I put it down as "UNKNOWN."