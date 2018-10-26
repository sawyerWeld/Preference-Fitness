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
The Mallows model has two parameters: the 'mean' ranking µ, and the variance ϕ. ϕ is a float and can be adjusted by selecting a float from a uniformly random distribution and adding it to ϕ. Generating a new central ranking given the current ranking R works as follows:

```
Do:
  α = Random_Int(0, Length(R))
  β = Random_Int(0, Length(R))
  
```

#### Plackett-Luce







