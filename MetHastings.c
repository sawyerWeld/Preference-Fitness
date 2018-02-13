// Compile with 'gcc MetHastings.c -std=c99'
// TODO: Add random seed

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

double values[2][100];
int values_size = 100;

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
double randNegOnetoOne(){ 
	return -1 + (2 * (double)rand()/RAND_MAX);
}

double gaussianCostFunction(double params[], int num_params) {
	double theta = params[0];
	double loss = 0;
	for (int i = 0; i < values_size; i++) {
		double temp = (theta * values[1][i]) - values[0][i];
		loss += temp * temp;
	}
	printf("%f\t%f\n",theta,loss);
	return loss;
	//loss(theta,x[],y[]) = sum over i ((theta * x[i]) - y[i])
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
			cur_params[i] = params[i] + randNegOnetoOne();
		}

		double cur_cost = cost_model(cur_params,num_params);

		double u = (randNegOnetoOne()+1)/2;
		
		// Acceptance Ratio
		double alpha = cur_cost / prev_cost;

		//printf("\nalpha\t%f\t%f\n",alpha,u);

		if (alpha > u) { //accepted
			
			//memcpy(samples[step+1],cur_params,num_params*sizeof(double));
			// set params to cur_params
			memcpy(params,cur_params,num_params*sizeof(double));
			// set prev_cost to cur_cost
			prev_cost = cur_cost;
		} else { // denied
			printf("denied\n");
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

	FILE *f=fopen("data.txt","r");
 
    if(f==NULL){
    	printf("no input file found\n");
        return 1;
    }
    for(int i = 0; i < 100; ++i) {
		values[0][i] = i;
    	fscanf(f, "%lf",&values[1][i]);
    	//printf("%d\t%lf\n",i,values[1][i]);
    }

     
 
    //close(f);

    // mcmc stuff

	double starting_params[] = {1};
    metHastings(gaussianCostFunction,starting_params,1,200,0);
    return 0;
}

