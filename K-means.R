# https://archive.ics.uci.edu/ml/datasets/Wholesale+customers

df <- read.csv('Wholesale customers data.csv', stringsAsFactors = F, header = T)
library(dplyr)
head(df)
colSums(is.na(df))
summary(df)
boxplot(df[,3:ncol(df)])
options(scipen = 100)
boxplot(df[,3:ncol(df)])

temp <- NULL
for (i in 3:ncol(df)) {
  temp <- rbind(temp, df[order(df[,i], decreasing = T),] %>% slice(1:5))
}
temp %>% arrange(Fresh) %>% head()

temp <- distinct(temp)
df.rm.outlier <- anti_join(df, temp)

par(mfrow = c(1,2))
boxplot(df[,3:ncol(df)])
boxplot(df.rm.outlier[,3:ncol(df)])
dev.off()

#Elbow method
install.packages("factoextra")
library(factoextra)
set.seed(2021)
fviz_nbclust(df.rm.outlier[,3:ncol(df.rm.outlier)], kmeans method = "wss", k.max = 15) +
  theme_minimal() +
  ggtitle("Elbow Method")

#Silouette method
fviz_nbclust(df.rm.outlier[,3:ncol(df.rm.outlier)], kmeans, method = "silhouette", k.max = 15) +
  theme_minimal() +
  ggtitle("Silhouette Plot")

#create K-means model
df.kmeans <- kmeans(df.rm.outlier[,3:ncol(df.rm.outlier)], centers = 5, iter.max = 1000)
df.kmeans
#Visualization
barplot(t(df.kmeans$centers), beside=TRUE, col = 1:6)
legend("topleft", colnames(df[,3:8]), fill = 1:6, cex = 0.5)

df.rm.outlier$cluster <- df.kmeans$cluster
head(df.rm.outlier)
