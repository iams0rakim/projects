#Hierarchical clustering

df <- USArrests
head(df)
colSums(is.na(df))
summary(df)
boxplot(df)
library(dplyr)
df <- scale(df) %>% as.data.frame()
boxplot(df)
library(tibble)
df.rm.outlier <- df %>% rownames_to_column('rname') %>%
  arrange(desc('Rape')) %>%
  slice(-1:-2) %>%
  column_to_rownames('rname')
boxplot(df.rm.outlier)

#Analysis
df.dist <- dist(df.rm.outlier, method = "euclidean")
df.hclust.sing <- hclust(df.dist, method = "single")
df.hclust.cplt <- hclust(df.dist, method = "complete")
df.hclust.avg <- hclust(df.dist, method = "average")
df.hclust.cent <- hclust(df.dist, method = "centroid")
df.hclust.ward <- hclust(df.dist, method = "ward.D2")

plot(df.hclust.sing, cex = 0.6, hang = -1)
rect.hclust(df.hclust.sing, k = 4, border = 2:5)
plot(df.hclust.cplt, cex = 0.6, hang = -1)
rect.hclust(df.hclust.cplt, k = 4, border = 2:5)
plot(df.hclust.avg, cex = 0.6, hang = -1)
rect.hclust(df.hclust.avg, k = 4, border = 2:5)
plot(df.hclust.cent, cex = 0.6, hang = -1)
rect.hclust(df.hclust.cent, k = 4, border = 2:5)
plot(df.hclust.ward, cex = 0.6, hang = -1)
rect.hclust(df.hclust.ward, k = 4, border = 2:5)

df.clusters <- cutree(df.hclust.ward, k = 4)
table(df.clusters)
df.rm.outlier$cluster <- df.clusters
head(df.rm.outlier)
library(factoextra)
fviz_cluster(list(data = df.rm.outlier[,1:ncol(df.rm.outlier)-1], cluster = df.clusters))

library(reshape2)
temp <- df.rm.outlier %>% melt(id = 'cluster')
head(temp)
df.means <- dcast(temp, cluster ~ variable, mean)
df.means
barplot(t(df.means[,1]), beside=TRUE, col = 1:4, names.arg = c(1:4))
legend("topright", colnames(df.rm.outlier[1:4]), fill = 1:4, cex = 0.5)