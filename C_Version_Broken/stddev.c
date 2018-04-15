#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#define _2PI 6.28318530718

double uniform(double min, double max) {
    if (min >= max) return 0;
    double zeroOne = (double)rand()/RAND_MAX;
    return min + ((max - min) * zeroOne);
}

double box_meuller(double sigma, double mu) {
    double u = uniform(0,1);
    double v = uniform(0,1);
    double r = sqrt(-2 * log(u));
    double theta = _2PI*v;
    double Z1 = r*sin(theta);
    //double Z2 = r*cos(theta);
    return Z1 * sigma + mu;
}

double box_meuller2(double sigma, double mu) {
    double u,v,s;
    do {
        u = uniform(-1,1);
        v = uniform(-1,1);
        s = (u*u) + (v*v); 
    } while(s == 0 || s >= 1);
    double temp = sqrt((-2 * log(s))/s);
    double Z1 = u * temp;
    //double Z2 = v * temp;
    return Z1 * sigma + mu;
}

int mainnvm() {
    time_t t;
	srand((unsigned) time(&t));

    for (int i = 0; i < 100; i ++) {
        double result = box_meuller2(1,0);
        printf("%f\n",result);        
    }
}