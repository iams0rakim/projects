head(iris)
colSums(is.na(iris))
summary(iris)
boxplot(iris[,1:4])

#PCA
iris.pca <- prcomp(iris[1:4], center = T, scale. = T)
summary(iris.pca)
iris.pca$rotation #eigenvector
head(iris.pca$x, 10)
plot(iris.pca, type = 'l', main = 'Scree Plot')

#dimension reduction
head(iris.pca$x[,1:2], 10)
#visualization
install.packages('ggfortify')
library(ggfortify)
autoplot(iris.pca, data = iris, colour = 'Species')
