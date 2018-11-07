num <- 200
x <- 1:num
y <- rnorm(num, mean = 18, sd = 0.1)
z = x+y

capture.output(cat(z,sep="\n"), file = "mean0sd0_1.txt")