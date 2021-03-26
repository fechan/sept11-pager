# sept11-pager
This repository contains a CSV and JSON version of the all_messages pager logs provided in the [9/11 pager logs](https://911.wikileaks.org/files/index.html) released by Wikileaks in 2009. These logs contain pager messages from 3 AM EDT on September 11, 2001 to 3 AM the following day. I reccommend watching [this short YouTube documentary](https://www.youtube.com/watch?&v=inigBzDU8mw) about the 9/11 pager leaks as a primer to give this data some context.

I had to do a bit of guesswork with these field names, since I do not have a comprehensive reference and I have never used a pager myself. If you have ideas or clarification, please add your suggestion in the repo's GitHub Issues page.

|Field name|Format|Description|
|---|---|---|
|date|YYYY-MM-DD|Date when the message was received|
|time|HH:MM:SS|Time when the message was received, in 24-hour format. Single digits are preceded by a 0|
|network|string|Name of the carrier network|
|capcode|number|CAP code/pager number of the recipient's pager|
|time2|HH:MM:SS AM/PM|Not sure. In 12-Hour AM/PM format. Single digits are *not* preceded by anything. Seems to be ~3 hours off of `time`, and only appears at the end of Metrocall multipart messages.|
|pocsag_mode|1, 2, or 3|Not sure. Only exists if the pager message uses the POCSAG protocol. Mutually exclusive with `function`, `mode`, and `time2`|
|pocsag_rate|1200 or 2400|POCSAG data rate, in bits per second|
|function|A, B, C, or D|Not sure. Probably corresponding to the ABCD dial on a pager.|
|mode|string|Type of message. ALPHA = alphanumeric, ST/SF NUM = numeric, TONE = beep, etc.|
|content|string|Message content|
