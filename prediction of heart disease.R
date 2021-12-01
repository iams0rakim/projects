library(caret)
rawdata <- read.csv(file="heart.csv", header=TRUE)
str(rawdata)
rawdata$target <- as.factor(rawdata$target)
unique(rawdata$target)
rawdata$age<-scale(rawdata$age)
rawdata$trestbps<-scale(rawdata$trestbps)
rawdata$chol<-scale(rawdata$chol)
rawdata$thalach<-scale(rawdata$thalach)
rawdata$oldpeak<-scale(rawdata$oldpeak)
rawdata$slope<-scale(rawdata$slope)
newdata<-rawdata
factorVar <- c("sex", "cp", "restecg", "exang", "ca", "thal")
newdata[, factorVar] = lapply(newdata[, factorVar], factor)
set.seed(2020)
datatotal<-sort(sample(nrow(newdata), nrow(newdata)*0.7))
train<-newdata[datatotal,]
test<-newdata[-datatotal,]
train_x<-train[,1:12]
train_y<-train[,13]
test_x<-test[,1:12]
test_y<-test[,13]
ctrl <- trainControl(method="repeatedcv", repeats = 5)
logitFit <- train(target ~ .,
                  data = train,
                  method = "LogitBoost",
                  trControl = ctrl,
                  metric = "Accuracy")
logitFit
plot(logitFit)

#Prediction
pred_test <- predict(logitFit, newdata=test)
confusionMatrix(pred_test, test$target)
#importance
importance_logit <- varImp(logitFit, scale=FALSE)
plot(importance_logit)
