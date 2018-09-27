setwd("~/GitHub/Thesis/Plotting")
library(ggplot2)

data <- read.table("../data_output/PL-data.txt",header = FALSE)
PLScores <- as.numeric(data[,6])
Iteration <- 1:length(PLScores)
df <- data.frame(PLScores, Iteration)
# plot(PLScores, type="o")
ggplot(data = df, aes(x=Iteration,y=PLScores, group=1))+
  geom_line() +
  geom_point()
