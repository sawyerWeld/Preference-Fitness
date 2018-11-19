# Simple Bar Plot

sets <- c(1:30)
mals <- fits$Mallows
pla  <- fits$Plackett.Luce
values <- c(log10(mals), log10(pla))
Model <- c(rep("Mallows",30), rep("Plackett-Luce",30))
mydata <- data.frame(sets, values)

p <-ggplot(mydata, aes(sets, values))
p + geom_bar(stat = "identity", aes(fill = Model), position = "dodge") +
  xlab("Datasets") + ylab("Log10 of Fit") + 
  theme(panel.background = element_blank())
#  theme_bw() + 
  + theme(legend.position = "none")
