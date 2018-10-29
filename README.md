### Immediate Issues
**The biggest issue I have is with the dispersion parameter in the Mallow's Model. I understand that this parameter indicates dispersion in the data, but im not sure what the relationship is or how to find it. When we generate data using the method from Lu & Boutillier 2014, we use a parameter eta in range 0 to 1 that determines how many times to swap two alternatives. I'm not sure what the relationship between phi and eta is, or if I can somehow find an estimation of eta directly from the data.**

# Empirical Analysis of Preference Model Fit

Analyzing the fit of various preference models on real-world data. This data includes data with ties or missing candidates.
The current focus is on the Plackett-Luce model and Mallow's Phi model. I'm hoping to have these done by November 19th so that I can submit incremental research to the FLAIRS32 conference. By then I will have the models programmed so that I can infer their parameters from the datasets and be able to generate new datasets given the models that I found. I will then have a method of comparing the difference between the generated dataset and the original data.

## Basic Terminology

* Ranking: And list of objects ordered by how desirable they are. ABC means the utility of A is greater than that of B and that of C, and that the utility of B is greater than that of C. ABC provides no information on how much greater A is than B or B is than C.

* Alternative: A candidate in the ranking. Alternative is an odd word to use for this but it frees up the word 'candidate' for use in the machine learning algorithms later.

## Models

### Mallows:

The Mallows modle is the preference modelling equivalent of a gaussian distribution. The mean is in this case a central ranking, denoted µ, is the ranking for which the sum distance from µ to every other ranking is minimized. 

Distance measure here is important. We are using the Kenall-Tau distance measure, which quantifies the minimium number of swappings of alternatives required to turn one ranking into the other.
For instance, ABC and ACB are 1 unit apart, the relationship between B and C has swapped. ABC and ABD are also 1 unit of distance apart, as the relationships between (A and B) and C have changed by 1/2 each. They've gone from greater than to no informaiton, which is 1/2 unit of distance each.

There is a second parameter, ϕ, which indicates the dispersion of the data. I need to explore this parameter further. **todo**

### Plackett-Luce:

The Plackett-Luce model relies on a set of parameters known as weights. The weight vector, denoted herewithin as W, contains one weight for every alternative in the dataset. The weight for alternative i, W<sub>i</sub>, tells us how prefered alternative i is. The larger the weight, the more preferred the alternative it corresponds to is.

The probability of a given ranking, ABC, is given as the sum of the probability of each individual relationship encoded within the preference. ABC implies A > B, A > C, and B > C. The probability of A being ranked first over B and C is the probability of A being ranked over B and C times the probability of B being ranked over C. This is given as
<p align="center">
  <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{W_A}{W_B&space;&plus;&space;W_C}&space;\times&space;\frac{W_B}  {W_C}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{W_A}{W_B&space;&plus;&space;W_C}&space;\times&space;\frac{W_B}{W_C}" title="\frac{W_A}{W_B + W_C} \times \frac{W_B}{W_C}" /></a>
</p align="center">
More generally, the probability of ordering O with weights W is given as
<p align="center">
  <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{W_0}{W_1&plus;\ldots&plus;W_{N-1}}\times\frac{W_1}{W_2&plus;\ldots&plus;W_{N-1}}\times\ldots\times\frac{W_{N-3}}{W_{N-2}&plus;W_{N-1}}\times\frac{W_{N-2}}{W_{N-1}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{W_0}{W_1&plus;\ldots&plus;W_{N-1}}\times\frac{W_1}{W_2&plus;\ldots&plus;W_{N-1}}\times\ldots\times\frac{W_{N-3}}{W_{N-2}&plus;W_{N-1}}\times\frac{W_{N-2}}{W_{N-1}}" title="\frac{W_0}{W_1+\ldots+W_{N-1}}\times\frac{W_1}{W_2+\ldots+W_{N-1}}\times\ldots\times\frac{W_{N-3}}{W_{N-2}+W_{N-1}}\times\frac{W_{N-2}}{W_{N-1}}" /></a>
</p align="center">

## Parameter Estimation

To estimate the parameters of the models given the data, we use the Metropolis-Hastings algorithm. The Metropolis algorithm is an MCMC method that works as follows: Generate a new set of parameters given the previous parameters. If the new parameters score better than the previous parameters (in the case of this implementation, lower is better), the new parameters are the new current parameters. If the new parameters are not better, they can still be set as the new parameters; the probability of accepting the new candidates when they are worse than the current parameters is proportional to the ratio of the new paramters to the current parameters.

```
Current_Parameters = Random_Parameters

While (N < Number_of_Iterations):
  New_Parameters = Generate_Candidate(Current_Parameters)
  
  Current_Score = Loss_Function(Current_Parameters)
  New_Score = Loss_Function(New_Parameters)
  
  α = New_Score / Current_Score
  u = Uniform_Random(0, 1)
  
  if (α ≥ u):
    Current_Parameters = New_Parameters
```

### Generating New Candidates
The Generate_Candidate function serves to create a new set of parameters given the current parameters. The candidate generation function,when applied multiple times, must have a non-zero probability of generating any set of parameters or else it would violate ergodic principles. 

#### Mallows Model
The Mallows model has two parameters: the 'mean' ranking µ, and the variance ϕ. 

**This next paragraph needs revision. Do I actually use the Metropolis algorithm to find phi? I know it indicates the spread of the data, but I'm not sure how exactly that works and I'm not sure the relationship between phi here and eta in the mallows dataset generation model.**
ϕ is a float and can be adjusted by selecting a float from a uniformly random distribution and adding it to ϕ. 

Generating a new central ranking given the current ranking R works as follows:

```
Do:
  α = Random_Int(0, Length(R))
  β = Random_Int(0, Length(R))
  Swap_in_Place(R[α], R[β])
While (Uniform_Random(0, 1) > Tuning_Parameter)
```

The tuning parameter is used to tweak how far from the current parameters the new parameters will be. The lower the tuning parameter, the higher the Kendall-Tau distance from the current parameters to the new parameters.

#### Plackett-Luce
The parameters of the Plackett-Luce model are a vector of weights corresponding to each alternative in the dataset. The sum of the vector is 1.0. We generate a new candidate vector by moving mass from one alternative to another in the weight vector W as follows:

```
Index_I = Random_Int(0, Length(R))
Index_J = Random_Int(0, Length(R))

While(Index_I == Index_J):
  Index_J = Random_Int(0, Length(R))
  
I = W[Index_I]
J = W[Index_J]

Transfer_Limit = Minimum(I, 1.0 - J)
Transfer_Amount = Transfer_Limit * Tuning_Parameter

W[Index_I] -= Transfer_Amount
W[Index_J] += Transfer_Amount
```

### Cost Functions
The Cost_Function function serves to score the current set of parameters against the dataset. The cost of one set of parameters does not tell us much, but by comparing the cost of two sets of parameters against each other, we can determine which set of parameters better fits the dataset.

#### Mallows Model
To find the central ranking of a Mallows model we seek to minimize the distance between the central ranking, µ, to every ranking present in the dataset. Therefore the cost function on a set of orderings O is:

<p align = "center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{o&space;\in&space;O}KT(\mu,o)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{o&space;\in&space;O}KT(\mu,o)" title="\sum_{o \in O}KT(\mu,o)" /></a>
</p align = "center">

Where Kendall-Tau distance is defined as:
<p align = "center">
<a href="https://www.codecogs.com/eqnedit.php?latex=KT(\mu,o)&space;=&space;\sum_{&space;\{&space;i,j\}&space;\in&space;{\mu&space;\choose&space;2}}&space;[&space;\{&space;Index(\mu,i)&space;-&space;Index(u,j)&space;\}&space;\times&space;\{&space;Index(o,i)&space;-&space;Index(o,j)&space;\}&space;]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?KT(\mu,o)&space;=&space;\sum_{&space;\{&space;i,j\}&space;\in&space;{\mu&space;\choose&space;2}}&space;[&space;\{&space;Index(\mu,i)&space;-&space;Index(u,j)&space;\}&space;\times&space;\{&space;Index(o,i)&space;-&space;Index(o,j)&space;\}&space;]" title="KT(\mu,o) = \sum_{ \{ i,j\} \in {\mu \choose 2}} [ \{ Index(\mu,i) - Index(u,j) \} \times \{ Index(o,i) - Index(o,j) \} ]" /></a>
</p align = "center">

This does not cover the case where the value of a relationship encoded in the first ranking cannot be found in the second ranking. We cover this as follows:
```
try:
  // Kendall Tau Code
catch:
  kt += 0.5
```

## How to generate datasets given estimated parameters
todo
## How to determine the similarity of the generated dataset and the true data
todo
Apples to apples comparison
Iterate over every possible ranking (12!), summing the difference between P(ranking) in the generated set and the true set.










