// Util functions for normal distribution

// Need to make this work without values[]

// loss(theta,x[],y[]) = sum over i ((theta * x[i]) - y[i])
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
}