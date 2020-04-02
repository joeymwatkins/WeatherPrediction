# Title     : TODO
# Objective : TODO
# Created by: themi
# Created on: 4/2/2020
usePackage <- function(p) {
    if (!is.element(p, installed.packages()[,1]))
        install.packages(p, dep = TRUE)
    require(p, character.only = TRUE)
}

usePackage("randomForest")
usePackage("caTools")


data <- read.csv("processed_CR6Series_TenMin.csv")
data <- data[-1]
data <- data[, -which(names(data) %in% c("min_AirTC_Avg", "max_AirTC_Avg"))]

set.seed(123)
split <- sample.split(data$AirTC_Avg, SplitRatio = 0.75)
training_set <- subset(data, split == TRUE)
test_set <- subset(data, split == FALSE)

classifier <- randomForest(x = training_set[, -which(names(data) %in% "AirTC_Avg")],
                           y = training_set$AirTC_Avg,
                           ntree = 5000, random_state = 0)

predictions <- predict(classifier, newdata = test_set[, -which(names(data) %in% "AirTC_Avg")])

correct <- predictions == test_set$AirTC_Avg
accuracy <- prop.table(table(correct))

confusionMatrix <- table(pred = predictions, Actual = test_set$AirTC_Avg)

print(confusionMatrix)
print(round(accuracy * 100, 2))

accuracy <- unname(accuracy["TRUE"])
