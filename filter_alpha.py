import csv
import re

with(open("messages_all.txt.csv", "r")) as all_msgs_file:
    all_msgs = csv.reader(all_msgs_file)
    with(open("messages_all.txt.alphaonly.csv", "w")) as alpha_msgs_file:
        alpha_msgs = csv.writer(alpha_msgs_file)
        for message in all_msgs:
            if message[9] == "ALPHA" and re.match(".*[a-zA-Z].*", message[10]):
                alpha_msgs.writerow(message)