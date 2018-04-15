setwd("C:/Thesis/Thesis") # Desktop

library(ggplot2)

data <- read.table("cosine_vs_ktau.txt",header = FALSE)

kt <- data[[1]]

cos <- data[[2]]

qplot(kt,cos)
