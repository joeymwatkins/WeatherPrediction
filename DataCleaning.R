pacman::p_load(tidyverse, readr, lubridate, stringr, dplyr)

url <- 'https://raw.githubusercontent.com/joeymwatkins/WeatherPrediction/master/processable_CR6Series_TenMin.csv'
weather <- read_csv(url)

weather_fixed <- weather %>%
  mutate(TIMESTAMP = str_sub(TIMESTAMP, 1, 9)) %>%
  group_by(TIMESTAMP) %>%
  filter(AirTC_Avg == max(AirTC_Avg)) %>%
  mutate(AirTF_Avg = (AirTC_Avg * 9/5 + 32)) %>%
  select(-AirTC_Avg)
  
write_csv(weather_fixed,
          "C:\\Users\\K-Squeezy\\Desktop\\SchoolFiles\\MachineLearning\\FinalProject\\daily_high_temps.csv")
         