#include <stdio.h>
#include <math.h>

# define LEN 5

struct ordering {
    int arr[LEN];
    int len;
};

int tau(struct ordering a, struct ordering b) {
    if (a.len != b.len) {
        printf("Unable to compute ktdistance: invalid lenghts");
        return -1;
    }
    //printf("lens: %d %d\n",a.len,b.len);
    int count = 0;
    for (int i = 0; i < a.len; i++) {
			for (int j = i; j < a.len; j++) { 
				// every combination of alternatives
				int first = (a.arr[i] > b.arr[j]) ? 1 : 0;
				int secnd = (a.arr[j] > b.arr[i]) ? 1 : 0;
                //printf("%d %d %d %d\n",a.arr[i],b.arr[j],first,secnd);
				if (first != secnd)
					count ++;
			}
		}
    return count;
}

double normalize_kt(int dist, int length) {
    double d = (double) dist;
	double l = (double) length;
    return (d*2.0 / (l * (l-1)));
}

// P (pi | sigma, theta)
// mode is sigma, dispersion is theta
double mallows_prob(struct ordering mode, struct ordering pi, int dispersion) {
    double zed = -1; // Z(mode,dispersion) : some normalization constant
    double hmm = exp(-1 * dispersion * tau(mode, pi));
    return (1 / zed) * hmm;
}



int main() {
    int arr1[] = {1,2,3,4,5};
    int arr2[] = {3,4,1,2,5};
    int order_len = 5;
    struct ordering a = {arr1[order_len], order_len};
    struct ordering b = {arr2[order_len], order_len};
    a.len = order_len;
    b.len = order_len;
    int dist = tau(a,b);
    double norm = normalize_kt(dist, order_len);
    printf("%d\t%g\n",dist,norm);
    return 0;
}
