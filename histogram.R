#setwd("~/Desktop/thesis/Thesis") # Laptop

data <- read.table("data.txt",header = FALSE)

Dispersion <- matrix(data = NA, nrow = dim(data)[1], ncol = dim(data)[2])

for (i in 1:dim(data)[2]) {
  Dispersion[,i] <- c(as.numeric(data[[i]]))
}

hist(Dispersion, breaks = 200, main = "Parameter Estimate")
