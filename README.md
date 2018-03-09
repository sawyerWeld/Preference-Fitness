# Parameter Estimation of Preference Models

### Current Goal

Estimate parameteres with the Metropolis algorithm. Currently can estimate mallows model parameters or standard deviations of a distribution. Current goal is to make this generic, so that it can search a space for any sort of model with parameters and cost function.

### Development Notes

To make the MH alg generic we should do the following:

Create a state struct, which stores a void** of params

This may not be necessary due to the shift function
/*Create a function for each 'use' of the MH alg which casts the params in the state as is necessary where 'use' is a use case such as finding standardd deviation of a normal distribution or finding the dispersion and centroid of a mallows model*/

Create a function for each use of the MH alg which generates a candidate from the current state.

For the normal distribution this would look like
- shiftFuncGauss(&state):
    shift_by_std_deviate(*(double*) state.params[0])

For the mallows model this would look like
- shiftMallows(&state):
    shift_ordering(*(ordering*) state.params[0])
    shift_by_std_deviate(*(double*) state.params[1])
