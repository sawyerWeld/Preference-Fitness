data <- read.table("outputfile.txt",header = FALSE)

dataNum <- matrix(data = NA, nrow = dim(data)[1], ncol = dim(data)[2])

for (i in 1:dim(data)[2]) {
  dataNum[,i] <- c(as.numeric(data[[i]]))
}

hist(dataNum)