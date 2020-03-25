pacman::p_load(tidyverse, readr, lubridate, stringr, dplyr)

url <- 'https://raw.githubusercontent.com/joeymwatkins/WeatherPrediction/master/processable_CR6Series_TenMin.csv'
weather <- read_csv(url)

weather_fixed <- weather %>%
  mutate(TIMESTAMP = str_replace_all(TIMESTAMP, " ", "   ")) %>%
  mutate(TIMESTAMP = str_sub(TIMESTAMP, 1, 10)) %>%
  group_by(TIMESTAMP) %>%
  filter(AirTC_Avg == max(AirTC_Avg)) %>%
  mutate(AirTF_Avg = (AirTC_Avg * 9/5 + 32)) %>%
  select(-AirTC_Avg)

weather_fixed_new <- distinct(weather_fixed)
  
write_csv(weather_fixed,
          "C:\\Users\\K-Squeezy\\Desktop\\SchoolFiles\\MachineLearning\\FinalProject\\daily_high_temps.csv")

write_csv(weather_fixed_new,
          "C:\\Users\\K-Squeezy\\Desktop\\SchoolFiles\\MachineLearning\\FinalProject\\daily_high_temps_distinct.csv")
