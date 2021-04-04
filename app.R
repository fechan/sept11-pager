library(shiny)
library(dplyr)
library(stringr)
library(DT)

messages <- read.csv("messages_all.txt.csv") %>% filter(mode == "ALPHA")

capcode_message_count <- messages %>%
  group_by(capcode) %>%
  summarize(num_messages = n())

first_messages <- messages %>%
  distinct(capcode) %>%
  left_join(capcode_message_count) %>%
  left_join(messages[!duplicated(messages$capcode),] %>% select(capcode, content))

ui <- navbarPage(title = "9/11 Pager Data Explorer",
  tabPanel("All messages",
    fluidRow(
      column(12, DTOutput("messages"))
    )
  ),
  tabPanel("First messages",
    fluidRow(
      column(12, DTOutput("first_messages"))
    )
  )
)

server <- function(input, output) {
  output$messages <- renderDT(messages)
  output$first_messages <- renderDT(first_messages)
}

shinyApp(ui = ui, server = server)