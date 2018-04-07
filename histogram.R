#setwd("~/Desktop/thesis/Thesis") # Laptop
setwd("C:/Thesis/Thesis") # Desktop

data <- read.table("pythontest.txt",header = FALSE)

Dispersion <- matrix(data = NA, nrow = dim(data)[1], ncol = dim(data)[2])

for (i in 1:dim(data)[2]) {
  Dispersion[,i] <- c(as.numeric(data[[i]]))
}

hist(dataNum, breaks = 200, main = "Parameter Estimate")
