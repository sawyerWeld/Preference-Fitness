// Util functions for mallows model
// Needs ktau.c

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

