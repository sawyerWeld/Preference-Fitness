// Compile with 'gcc MetHastings.c -std=c99'
// TODO: Add random seed, create normal distribution

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

//	Placeholder method of same signature as mallows just for testing
//	Returns the sum of doubles in nums[]
//	len is the length of nums[]
double addList(double nums[], int len) {
	double sum = 0;
	for(int i = 0; i < len; i++) {
		sum += nums[i];
	}
	return sum;
}

// normal random [0:1]
double randZeroOne(){ 
	return (double)rand()/RAND_MAX;
}

double gaussianCostFunction(double a, double b) {
	// unsure how this works, but part should look like this
	return -1 * (a * a) + (b * b);
}

// cost_model : the function to find distribution of
// params[] : the starting parameters. might be nice to set them manually?
// num : the number of parameters
// runs : how many runs to perform
// todo: add burn in

void metHastings(double(cost_model)(double[],int), double params_[], int num, int runs) {

	int N = runs;
	int step = 0; // using steps in a while to make burn in easier to implement
	double samples[N][num]; // needs to be 2d, with params.len cols

	double params[num]; 
	memcpy(params,params_,num*sizeof(double));

	for (int i = 0; i < num; i++) {
		samples[0][i] = params[i];
	}

	while (step != N-1) { // check for off by one errors
		double prev_cost = cost_model(samples[step],num);


		// Slightly alter the parameters so we can explore the space
		// this is poor code, but im not sure ~how~ the space should
		// be explored, so i've left it as a placeholder for now.
		// I'm thinking the best way would be to sample a gaussian
		// with center on the parameter and s.d. something like .05
		double cur_params[num];
		for (int i = 0; i<num; i++) 
			cur_params[i] = samples[step][i]+randZeroOne()-randZeroOne();

		double cur_cost = cost_model(cur_params,num);

		double u = randZeroOne();
		
		// Acceptance Ratio
		double alpha = cur_cost / prev_cost;

		if (alpha > u) { //accepted
			memcpy(samples[step+1],cur_params,num*sizeof(double));
		} else { // denied
			memcpy(samples[step+1],samples[step],num*sizeof(double));
		}
		step++;
	}


	printf("Run #\tParameters to cost function\t\n");
	for (int i = 0; i < N; i++) {
		printf("%d:\t", i);
		for (int j = 0; j < num; j++) {
			printf("%f\t",samples[i][j]);
		}
		printf("\n");
	}

	return;
}

int main() {

	// read list of [1:100] with gauss noise

	 FILE *f=fopen("data.txt","r");
 
    if(f==NULL){
    	printf("no file found\n");
        return 1;
    }
 
    double values[100];        
 
    for(int i = 0; i < 100; ++i) {
        fscanf(f, "%lf",&values[i]);
        //printf("%lf\n",values[i]);
     }

     
 
    //close(f);

    // mcmc stuff

	double starting_params[] = {1,1,1};
    metHastings(addList,starting_params,3,20);
    return 0;
}

