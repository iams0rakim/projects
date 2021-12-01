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

#image
install.packages('jpeg')
library(jpeg)
cat <- readJPEG('cat.jpeg')
class(cat)
dim(cat)
r <- cat[,,1]
g <- cat[,,2]
b <- cat[,,3]
cat.r.pca <- prcomp(r, center = F)
cat.g.pca <- prcomp(g, center = F) 
cat.b.pca <- prcomp(b, center = F)
rgb.pca <- list(cat.r.pca, cat.g.pca, cat.b.pca)

pc <- c(2,10,50,100,300)
for (i in pc) {
  pca.img <- sapply(rgb.pca, function(j) {
    compressed.img <- j$x[,1:i] %*% t(j$rotation[,1:i])
  }, simplify = 'array')
  writeJPEG(pca.img, paste('cat_pca_', i, '.jpeg', sep = ''))
}