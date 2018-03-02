// Compile with 'gcc MetHastings.c -std=c99'
// TODO: Add random seed

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "stddev.c"
#include "ktau.c"

double values[2][100];
int values_size = 100;

struct ordering orderings[100];
int orderings_size = 100;

struct ordering mu;

// normal random [0:1]
double randNegOnetoOne(){ 
	return -1 + (2 * (double)rand()/RAND_MAX);
}

double gaussianCostFunction(double params[], int num_params) {
	double theta = params[0];
	double loss = 0;
	for (int i = 0; i < values_size; i++) {
		double temp = (theta * values[1][i]) - values[0][i];
		if (1) {
			loss += temp * temp;
		} else {
			// Absolute value rather than squared
			temp *= (temp < 0) ? -1 : 1;
			loss += temp;
		}
		
	}
	//printf("%f\t%f\n",theta,loss);
	return loss;
	//loss(theta,x[],y[]) = sum over i ((theta * x[i]) - y[i])
}

//int arr1[] = {1,2,3,4,5};
//struct ordering mu = {arr1[5], 5};
//mu.len = 5;

// likelihood (succ | mu_hat, phi_hat) is proportional to
//    Sum over all i in succ (exp (-1 * phi_hat * tau(succ[i],mu_hat)))
double mallowsCostFunction(double params[], int num_params {
	double mu__ = params[0];
	double phi = params[1];
	double sum = 0;
	for (int i = 0; i < orderings_size; i++) {
		double temp = exp(-1 * phi * tau(mu,mu));
	}
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
		for (int i = 0; i<num_params; i++) {
			//cur_params[i] = samples[step][i]+randNegOnetoOne();
			//cur_params[i] = params[i] + randNegOnetoOne() * 0.1;
			cur_params[i] = params[i] + box_meuller2(.5,0);
		}

		double cur_cost = cost_model(cur_params,num_params);

		double u = (randNegOnetoOne()+1)/2;
		
		// Acceptance Ratio
		double alpha = prev_cost / cur_cost;

		//printf("\nalpha\t%f\t%f\n",alpha,u);

		if (alpha > u) { //accepted
			
			//memcpy(samples[step+1],cur_params,num_params*sizeof(double));
			// set params to cur_params
			memcpy(params,cur_params,num_params*sizeof(double));
			// set prev_cost to cur_cost
			prev_cost = cur_cost;
		} else { // denied
			//printf("denied\n");
			//memcpy(samples[step+1],samples[step],num_params*sizeof(double));
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

	int arr = {1,2,3,4,5};
    struct ordering mu = {arr[], 5};
	mu.len = 5;
 
    //close(f);


	double starting_params[] = {50};
    metHastings(gaussianCostFunction,starting_params,1,1000000,8000);
    return 0;
}

