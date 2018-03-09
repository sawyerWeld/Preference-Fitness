# Thesis
This space is for notes.

To make the MH alg generic we should do the following:

    - Create a state struct, which stores a void** of params

    - Create a function for each 'use' of the MH alg which casts the params in the state as is necessary where 'use' is a use case such as finding standardd deviation of a normal distribution or finding the dispersion and centroid of a mallows model

    - Create a function for each use of the MH alg which generates a candidate from the current state 
    

 

