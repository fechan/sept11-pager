"""
parse.py -- Parse pager logs from WikiLeaks' 2009 logs of pager transmissions around 9/11 into
CSV and JSON formats

Information about the original logs:
Date: year-month-day
Time: hour: min: sec
Network: Skytel / Arch / metrocall
Capcode: [########] (the address of the pager, or pagers the message is being sent to)
Function: A / B / C / D (POCSAG 0/1/2/3)
Mode: ST NUM (numeric), AF NUM (numeric), SH/TONE (tone), ALPHA (alphanumeric), BINARY, SECURE

Some pager transmissions contain multiple timestamps. The second one will contain
hour:minute:second AM/PM, and will be approximately 3 hours behind the first one.
I don't know what this second time represents.
"""
import re
import csv
import json

LOG_FILE_PATH = "messages_all.txt"

FIELDS = [
    "date",
    "time",
    "network",
    "capcode",
    "time2",
    "pocsag_mode",
    "pocsag_rate",
    "function",
    "mode",
    "content"
    ]
PAGER_MODES = ["ALPHA", "ST NUM", "SF NUM", "SH/TONE", "BINARY", "SECURE"]

pager_log_file = open(LOG_FILE_PATH)
pager_log = pager_log_file.read().splitlines()
pager_log_file.close()

failed_to_parse = []
parsed_messages = []

for raw_message in pager_log:
    message_parts = raw_message.split()
    message = {
        "date": message_parts[0],
        "time": message_parts[1],
        "network": message_parts[2],
        "capcode": re.sub("[^0-9]", "", message_parts[3])
    }
    if "{" in message_parts[3]: # If message uses POCSAG
        message["pocsag_mode"] = message_parts[4]
        message["pocsag_rate"] = message_parts[5]
        message["content"] = raw_message[raw_message.find(message_parts[5]) + len(message_parts[5]):] # Extract everything after rate string
    elif re.match("[0-9]{1,2}:[0-9]{2}:[0-9]{2}", message_parts[4]): # If the message has a second timestamp
        message["time2"] = f"{message_parts[4]} {message_parts[5]}"
        message["function"] = message_parts[6]
        message["mode"] = message_parts[7] # For some reason, this is always ALPHA
        message["content"] = raw_message[raw_message.find(message_parts[7]) + len(message_parts[7]):] # Extract everything after mode string
    else:
        message["function"] = message_parts[4]
        if message_parts[5] in ["ST", "SF"]:
            message["mode"] = message_parts[5] + " " + message_parts[6]
            message["content"] = raw_message[raw_message.find(message_parts[6]) + len(message_parts[6]):] # Extract everything after mode string
        else:
            message["mode"] = message_parts[5]
            message["content"] = raw_message[raw_message.find(message_parts[5]) + len(message_parts[5]):]
    message["content"] = message["content"].strip()

    # Do some validation
    if (("mode" in message and message["mode"] not in PAGER_MODES) or
            ("pocsag_rate" in message and message["pocsag_rate"] not in ["512", "1200", "2400"])):
        failed_to_parse.append(raw_message)
    else:
        parsed_messages.append(message)
print("Failed to parse the following messages:\n", "\n\n".join(failed_to_parse))

with open(LOG_FILE_PATH + ".json", "w") as jsonfile:
    json.dump(parsed_messages, jsonfile)

with open(LOG_FILE_PATH + ".csv", "w") as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=FIELDS)
    csvwriter.writeheader()
    for message in parsed_messages:
        csvwriter.writerow(message)