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


#linear SVM
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
svm_linear_fit <- train(Class ~ .,
                        data = train,
                        method = "svmLinear",
                        trControl = ctrl,
                        preProcess = c("center", "scale"),
                        metrics = "Accuracy")
pred_test <- predict(svm_linear_fit, newdata=test)
confusionMatrix(pred_test, test$Class)
importance_linear <- varImp(svm_linear_fit, scale=FALSE)
plot(importance_linear)

#non-linear SVM (Polynomial kernel)
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
svm_poly_fit <- train(Class ~ .,
                        data = train,
                        method = "svmPoly",
                        trControl = ctrl,
                        preProcess = c("center", "scale"),
                        metrics = "Accuracy")
svm_poly_fit
plot(svm_poly_fit)

pred_test <- predict(svm_poly_fit, newdata=test)
confusionMatrix(pred_test, test$Class)
importance_poly <- varImp(svm_poly_fit, scale=FALSE)
plot(importance_poly)
