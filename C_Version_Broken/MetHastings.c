// Compile with 'gcc MetHastings.c -std=c99'
// TODO: Add random seed

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "stddev.c"
#include "ktau.c"
#include "paramUtils.c"

double values[2][100];
int values_size = 100;

struct ordering orderings[100];
int orderings_size = 100;

struct ordering mu;

// normal random [0:1]
double randNegOnetoOne(){ 
	return -1 + (2 * (double)rand()/RAND_MAX);
}

// loss(theta,x[],y[]) = sum over i ((theta * x[i]) - y[i])
double gaussianCostFunction(double params[], int num_params) {
	double theta = params[0];
	double loss = 0;
	for (int i = 0; i < values_size; i++) {
		double temp = (theta * values[1][i]) - values[0][i];
		loss += temp * temp;
		//printf("%d\t%f\n",i,loss);
	}
	
	return loss;
}

// mu is the centroid, the center ordering in the distribution
// phi is dispersion, how far from mu things can go, like std dev in a gaussian
// likelihood (succ | mu_hat, phi_hat) is proportional to
//    Sum over all i in succ (exp (-1 * phi_hat * tau(succ[i],mu_hat)))
double mallowsCostFunction(double params[], int num_params) {
	double mu__ = params[0];
	double phi = params[1];
	double sum = 0;
	for (int i = 0; i < orderings_size; i++) {
		double temp = exp(-1 * phi * tau(mu,mu));
	}
	return sum;
}

// cost_model : the function to find distribution of
// params[] : the starting parameters. might be nice to set them manually?
// num : the number of parameters
// runs : how many runs to perform
// todo: add burn in
void metHastings(double(cost_model)(double[],int), double params_[], int num_params, int runs, int burn_in) {

	int N = runs;
	int step = 0; // using steps in a while to make burn in easier to implement
	//double samples[N][num_params]; // needs to be 2d, with params.len cols

	double params[num_params]; // parameters we search over
	memcpy(params,params_,num_params*sizeof(double));

	// for (int i = 0; i < num_params; i++) {
	// 	samples[0][i] = params[i];
	// }

	double prev_cost = cost_model(params,num_params); // need to set this to something


	FILE * fp;
   	fp = fopen ("outputfile.txt","w");

	while (step != N-1) { // using a while instead of a for bc i think it will be easier to add burn-in
		prev_cost = cost_model(params,num_params);
		//printf("\n%f\t%f\n",prev_cost,params);

		// todo update with comment block

		double cur_params[num_params];
		// we do this for doubles, need to specify
		for (int i = 0; i<num_params; i++) {
			cur_params[i] = params[i] + box_meuller2(.5,0);
		}

		// for params that are orderings we do this instead
		// while (weighted_coin() > uniform(0,1))
		// 	select 2 adjacent alternatives in the preference ordering
		//  swap them

		double cur_cost = cost_model(cur_params,num_params);

		double u = (randNegOnetoOne()+1)/2;
		
		// Acceptance Ratio
		double alpha = prev_cost / cur_cost;
		
		if (alpha > u) { //accepted
			memcpy(params,cur_params,num_params*sizeof(double));
			prev_cost = cur_cost;
		} else { // denied
		}
		if (step > burn_in)
			for (int i = 0; i < num_params; i++)
				fprintf(fp,"%f\n",cur_params[i]); // should look over all
		step++;
	}


	// Writing the output file	

	   //printf("Run #\tParameters to cost function\t\n");
	for (int i = 0; i < N; i++) {
		
		// for (int j = 0; j < num_params; j++) {
		// 	fprintf(fp,"%f, ",samples[i][j]);
		// }
		
	}

	fclose (fp);

	return;
}

int main() {
	time_t t;
	srand((unsigned) time(&t));


	// read list of [1:100] with gauss noise

	/* SD = 1.0 */
	FILE *f=fopen("data.txt","r");

	//FILE *f=fopen("mean0sd0_1.txt","r");
 
    if(f==NULL){
    	printf("no input file found\n");
        return 1;
    }
    for(int i = 0; i < 100; ++i) {
		values[0][i] = i;
    	fscanf(f, "%lf",&values[1][i]);
    	//printf("%d\t%lf\n",i,values[1][i]);
    }

	// close(f);

	// this doesnt do anything right now, but im thinking about mallows
	int arr[] = {1,2,3,4,5};
    struct ordering mu = {arr[5], 5};
	mu.len = 5;
	// mu here is the starting mu, ie starting_params[0]
	// dispersion is the second value
	// params needs to be made into void*
 
	void** param_list = {(void*) 10};
	struct state myparams = {param_list};
	myparams.len = 1;

	double starting_params[] = {1}; // set back to 50
	//printf("%f\n",gaussianCostFunction(starting_params,1));
    metHastings(gaussianCostFunction,starting_params,1,100000,20000);
    return 0;
}

