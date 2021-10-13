rawdata1 <- read.csv("university.csv", head=TRUE) #csv파일 읽기, head -> 제목 따올건지 여부(gre, toefl 등등)
str(rawdata1) #데이터의 대략적인 형태 확인
is.na(rawdata1$GRE.Score) #결측치 확인
sum(is.na(rawdata1$GRE.Score)) #결측치 갯수 확인
sum(is.na(rawdata1$TOEFL.Score))
sum(is.na(rawdata1$University.Rating))
sum(is.na(rawdata1$SOP))
sum(is.na(rawdata1$LOR))
sum(is.na(rawdata1$Research))
sum(is.na(rawdata1$Chance.of.Admit))

unique(rawdata1$GRE.Score) #변수 별 유니크값 확인
unique(rawdata1$TOEFL.Score)
unique(rawdata1$University.Rating)
unique(rawdata1$SOP)
unique(rawdata1$LOR)
unique(rawdata1$Research)
unique(rawdata1$Chance.of.Admit)

u_rating_table <- table(rawdata1$University.Rating)
u_rating_table

research_rating_table <- table(rawdata1$Research)
research_rating_table

max(rawdata1$Chance.of.Admit) #최댓값, 최솟값 확인하기
min(rawdata1$Chance.of.Admit)

par(mfrow=c(3,2), mar=c(5.1, 4.1, 4.1, 2.1)) #히스토그램 설정
hist(rawdata1$GRE.Score, main="GRE Score Histogram", xlab="GRE Score", col = "orange")
hist(rawdata1$TOEFL.Score, main="TOEFL Score Histogram", xlab="TOEFL Score", col = "green")
hist(rawdata1$SOP, main="SOP Score Histogram", xlab="SOP Score", col = "blue")
hist(rawdata1$CGPA, main="CGPA Score Histogram", xlab="CGPA Score", col = "darkmagenta")
hist(rawdata1$LOR, main="LOR Score Histogram", xlab="LOR Score", col = "yellow")
hist(rawdata1$Chance.of.Admit, main="Chance of Admit Histogram", xlab="Chance of Admit", col = "red")

par(mfrow=c(2,3), mar=c(2, 4.1, 4.1, 2.1)) #박스플랏 설정
boxplot(rawdata1$GRE.Score, main = "GRE Score box-plot", col = "orange")
boxplot(rawdata1$TOEFL.Score, main = "TOEFL Score box-plot", col = "green")
boxplot(rawdata1$SOP, main = "SOP Score box-plot", col = "blue")
boxplot(rawdata1$CGPA, main = "CGPA Score box-plot", col = "darkmagenta")
boxplot(rawdata1$LOR, main = "LOR Score box-plot", col = "yellow")
boxplot(rawdata1$Chance.of.Admit, main = "Chance of Admit box-plot", col = "red")

par(mfrow=c(1,2), mar=c(1,1,1,1))
pie(u_rating_table, main = "University Rating", radius = 1)
pie(research_rating_table, main = "Research", radius = 1)

plot(rawdata1)

#트레이닝 테스트 나누기(7:3)
set.seed(2020) #데이터 랜덤으로 뽑아도, 동일하게 뽑히게끔
newdata <- rawdata1
train_ratio <- 0.7 #트레이닝 데이터 비율 설정
datatotal <- sort(sample(nrow(newdata), nrow(newdata)*train_ratio)) #트레이닝 데이터에 속할 행(row) 선택
train <- newdata[datatotal,]
test <- newdata[datatotal,]

install.packages("caret", dependencies = TRUE) #머신러닝에 필요한 패키지 불러오기
library(caret)

ctrl <- trainControl(method = "repeatedcv", repeats = 5)
logistic_fit <- train(Chance.of.Admit ~., #타겟 ~ 피쳐
                      data = train, #학습 시킬 데이터
                      method = "glm", #학습 알고리즘
                      trControl = ctrl, #훈련 방법
                      preProcess = c("center", "scale"), #데이터 전처리
                      metric = "RMSE") #모형 평가 방법

logistic_fit
logistic_pred <- predict(logistic_fit, newdata = test) #예측하기

postResample(pred = logistic_pred, obs = test$Chance.of.Admit) #RMSE 구하기- postResampel 함수 이용하기
RMSE(logistic_pred, test$Chance.of.Admit) #RMSE 구하기- RMSE 함수 이용하기
sqrt(mean((logistic_pred - test$Chance.of.Admit)^2)) #RMSE 구하기- 직접 구하기

y_bar = mean(test$Chance.of.Admit) #R Squared 구하기
1 - sum((logistic_pred - test$Chance.of.Admit)^2 / sum((test$Chance.of.Admit-y_bar)^2))

MAE(logistic_pred, test$Chance.of.Admit) #MAE 구하기기
mean(abs(logistic_pred - test$Chance.of.Admit))

ctrl <- trainControl(method = "repeatedcv", repeats = 5)
logit_penal_fit <- train(Chance.of.Admit ~., #타겟 ~ 피쳐
                      data = train, #학습 시킬 데이터
                      method = "glmnet", #학습 알고리즘
                      trControl = ctrl, #훈련 방법
                      preProcess = c("center", "scale"), #데이터 전처리
                      metric = "RMSE") #모형 평가 방법
logit_penal_fit
logit_penal_pred <- predict(logit_penal_fit, newdata = test) #엘라스틱넷 회귀분석의 예측 및 평가
postResample(pred = logit_penal_pred, obs = test$Chance.of.Admit)

ctrl <- trainControl(method = "repeatedcv", repeats = 5)
rf_fit <- train(Chance.of.Admit ~., #타겟 ~ 피쳐
                data = train, #학습 시킬 데이터
                         method = "rf", #학습 알고리즘
                         trControl = ctrl, #훈련 방법
                         preProcess = c("center", "scale"), #데이터 전처리
                         metric = "RMSE") #모형 평가 방법
rf_fit #랜덤 포레스트
plot(rf_fit)

rf_pred <- predict(rf_fit, newdata=test) #예측 및 평가
postResample(pred = rf_pred, obs = test$Chance.of.Admit)

ctrl <- trainControl(method = "repeatedcv", repeats = 5)
svm_linear_fit <- train(Chance.of.Admit ~ ., #SVM 
                        data = train,
                        method = "svmLinear",
                        trControl = ctrl,
                        preProcess = c("center", "scale"),
                        metric = "RMSE")
svm_linear_fit

svm_linear_pred <- predict(svm_linear_fit, newdata = test) #예측 및 평가가
postResample(pred = svm_linear_pred, obs = test$Chance.of.Admit)

ctrl <- trainControl(method = "repeatedcv", repeats = 5)
svm_poly_fit <- train(Chance.of.Admit ~ .,
                      data = train,
                      method = "svmPoly",
                      trControl = ctrl,
                      preProcess = c("center", "scale"),
                      metric = "RMSE")
svm_poly_fit
plot(svm_poly_fit)

svm_poly_pred <- predict(svm_linear_fit, newdata=test)
postResample(pred = svm_linear_pred, obs = test$Chance.of.Admit)

rawdata2 <- read.csv("university.csv", head=TRUE) #회귀 말고 분류로 예측해보기
str(rawdata2)

par(mfrow=c(1,2), mar=c(5.1, 4.1, 4.1, 4.2)) #타겟 변수 살펴보기기
hist(rawdata2$Chance.of.Admit, main="Chance of Admit Histogram", xlab = "Chance of Admit", col = "red")
boxplot(rawdata2$Chance.of.Admit, main="Chance of Admit box-plot", col = "red")

summary(rawdata2$Chance.of.Admit) #타겟 변수 살펴보기 - 요약
target_median = median(rawdata2$Chance.of.Admit)
target_median

rawdata2[(rawdata2$Chance.of.Admit < target_median), "Chance.of.Admit"] = "0" #타겟 연속형 -> 범주형
rawdata2[(rawdata2$Chance.of.Admit >= target_median), "Chance.of.Admit"] = "1"

rawdata2$Chance.of.Admit <- as.factor(rawdata2$Chance.of.Admit) #타겟 변수를 팩터로 바꿔주기
str(rawdata2)

unique(rawdata2$Chance.of.Admit)
rawdata2

#트레이닝 데이터 나누기
set.seed(2020)
newdata2 <- rawdata2
train_ratio <- 0.7
datatotal2 <- sort(sample(nrow(newdata2), nrow(newdata2)*train_ratio))
train2 <- newdata2[datatotal2,]                   
test2 <- newdata2[datatotal2,]

#knn
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
customGrid <- expand.grid(k=1:20)
knn_fit2 <- train(Chance.of.Admit ~ .,
                  data = train2,
                  method = "knn",
                  trControl = ctrl,
                  preProcess = c("center", "scale"),
                  tuneGrid = customGrid,
                  metric = "Accuracy")
knn_fit2
plot(knn_fit2)
dev.off() #오류 나서 리셋 시킨 것

knn_pred2 <- predict(knn_fit2, newdata=test2)
confusionMatrix(knn_pred2, test2$Chance.of.Admit)

## Logit Boost
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
logit_boost_fit2 <- train(Chance.of.Admit ~ .,
                          data = train2,
                          method = "LogitBoost",
                          trControl = ctrl,
                          preProcess = c("center", "scale"),
                          metric = "Accuracy")

logit_boost_fit2
plot(logit_boost_fit2)

logit_boost_pred <- predict(logit_boost_fit2, newdata=test2)
confusionMatrix(logit_boost_pred, test2$Chance.of.Admit)

#Penalized Logistic
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
logit_plr_fit2 <- train(Chance.of.Admit ~ .,
                        data = train2,
                        method = "plr",
                        trControl = ctrl,
                        preProcess = c("center", "scale"),
                        metric = "Accuracy")
logit_plr_fit2
plot(logit_plr_fit2)

#예측해보기
logit_plr_pred <- predict(logit_plr_fit2, newdata = test2)
confusionMatrix(logit_plr_pred, test2$Chance.of.Admit)

#naive bayes
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
nb_fit2 <- train(Chance.of.Admit ~ .,
                 data = train2,
                 method = "naive_bayes",
                 trControl = ctrl,
                 preProcess = c("center", "scale"),
                 metric = "Accuracy")
nb_fit2
plot(nb_fit2)

#예측하기
nb_pred2 <- predict(nb_fit2, newdata = test2)
confusionMatrix(nb_pred2, test2$Chance.of.Admit)

#Ramdon Forest
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
rf_fit2 <- train(Chance.of.Admit ~ .,
                 data = train2,
                 method = "rf",
                 trControl = ctrl,
                 preProcess = c("center", "scale"),
                 metric = "Accuracy")
rf_fit2
plot(rf_fit2)

rf_pred2 <- predict(rf_fit2, newdata=test2) #예측하기
confusionMatrix(rf_pred2, test2$Chance.of.Admit)

#선형 서포트 벡터 머신
ctrl <- trainControl(method = "repeatedcv", repeats = 5)
svm_linear_fit2 <- train(Chance.of.Admit ~ .,
                         data = train2,
                         method = "svmLinear",
                         trControl = ctrl,
                         preProcess = c("center", "scale"),
                         metric = "Accuracy")
svm_linear_fit2

svm_linear_pred2 <- predict(svm_linear_fit2, newdata = test2)
confusionMatrix(svm_linear_pred2, test2$Chance.of.Admit)

ctrl <- trainControl(method = "repeatedcv", repeats = 5)
svm_poly_fit2 <- train(Chance.of.Admit ~ .,
                       data = train2,
                       method = "svmPoly",
                       trControl = ctrl,
                       preProcess = c("center", "scale"),
                       metric = "Accuracy")
svm_poly_fit2
plot(svm_poly_fit2)

#예측해보기
svm_poly_pred2 <- predict(svm_poly_fit2, newdata=test2)
confusionMatrix(svm_poly_pred2, test2$Chance.of.Admit)
