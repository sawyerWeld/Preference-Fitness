setwd("~/GitHub/Thesis/Plotting")
library(ggplot2)

data <- read.table("../data_output/PL-data.txt",header = FALSE)
PLScores <- as.numeric(data[,6])
print(length(PLScores))
# plot(PLScores, type="o")
ggplot(data = PLScores, aes())