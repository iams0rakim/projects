library(caret)
rawdata <- read.csv(file="wine.csv", header=TRUE)
rawdata$Class <- as.factor(rawdata$Class)
str(rawdata)
analdata <- rawdata
set.seed(2021)
datatotal <- sort(sample(nrow(analdata), nrow(analdata)*0.7))
train <- rawdata[datatotal,]
test <- rawdata[-datatotal,]
str(train)
train_x <- train[,1:13]
train_y <- train[,14]
test_x <- test[,1:13]
test_y <- test[,14]

install.packages("tree")
library(tree)
treeRaw <- tree(Class ~., data = train)
plot(treeRaw)
text(treeRaw)
cv_tree <- cv.tree(treeRaw, FUN=prune.misclass)
plot(cv_tree)
prune_tree <- prune.misclass(treeRaw, best=4)
plot(prune_tree)
text(prune_tree, pretty=0)

#Prediction
pred <- predict(prune_tree, test, type='class')
confusionMatrix(pred, test$Class)

#Random Forest
ctrl <- trainControl(method="repeatedcv", repeats=5)
rfFit <- train(Class ~ .,
               data = train,
               method = "rf",
               trControl = ctrl,
               preProcess = c("center", "scale"),
               metric="Accuracy")
rfFit
plot(rfFit)
#Prediction
pred_test <- predict(rfFit, newdata=test)
confusionMatrix(pred_test, test$Class)
#importance
importance_rf <- varImp(rfFit, scale = FALSE)
plot(importance_rf)
