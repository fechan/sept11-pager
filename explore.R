library(dplyr)
library(stringr)

messages <- read.csv("messages_all.txt.csv")
multipart_msgs <- messages %>%
  filter(str_detect(.data$content, regex("\\([0-9]\\/[0-9]\\)")))

most_messages <- messages %>%
  group_by(capcode) %>%
  arrange(nrow(filter(messages, capcode == capcode)), .by_group = TRUE)

capcode_message_count <- messages %>%
  filter(mode == "ALPHA") %>%
  group_by(capcode) %>%
  summarize(num_messages = n())

first_messages <- messages %>%
  filter(mode == "ALPHA") %>%
  distinct(capcode) %>%
  left_join(capcode_message_count) %>%
  left_join(messages[!duplicated(messages$capcode),] %>% select(capcode, content))