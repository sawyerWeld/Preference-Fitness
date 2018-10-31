
Apples to apples comparison
Iterate over every possible ranking (12!), summing the difference between P(ranking) in the generated set and the true set.
The dataset won't have all of the rankings, not even close to all of them. Perhaps something akin to laplace smoothing?

* The Laplace-smoothed probability of event a in probability distribution A is as follows:

<p align = "center">
<a href="https://www.codecogs.com/eqnedit.php?latex=P_{Laplace}(a)&space;=&space;\frac{freq(a)&space;&plus;&space;k}{size(A)&space;&plus;&space;(uniques(A)\times&space;k)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P_{Laplace}(a)&space;=&space;\frac{freq(a)&space;&plus;&space;k}{size(A)&space;&plus;&space;(uniques(A)\times&space;k)}" title="P_{Laplace}(a) = \frac{freq(a) + k}{size(A) + (uniques(A)\times k)}" /></a>
</p align = "center">

Where k is a parameter that determines how many times each possible event is added. As long as k is greater than or equal to 1, every event has non-zero probability. Increasing k causes the distribution to become more similar to the uniform distribution, but as long as we are consistent with the value of k across models, the results should be statistically valid. 
