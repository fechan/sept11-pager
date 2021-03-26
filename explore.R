library(dplyr)
library(stringr)

messages <- read.csv("messages_all.txt.csv")
multipart_msgs <- messages %>%
  filter(str_detect(.data$content, regex("\\([0-9]\\/[0-9]\\)")))