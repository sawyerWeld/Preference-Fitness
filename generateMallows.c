// Generate artificial data for the preference models

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

# define LEN 5

struct ordering {
    int arr[LEN];
    int len;
};

int zeroOdering(struct ordering * o) {
    for (int i = 0; i < o.len; i++)
        o.arr[i] = 0;
}

int printordering(struct ordering o) {
    for (int i = 0; i < o.len; i++) {
        printf("%d ",o.arr[i]);
    }
    printf("\n");
    return 0;
}


struct ordering generateMallows(double phi) {
    struct ordering a;
    a.len = LEN;
    zeroOdering(&a);
    a.arr[0] = 0;
    for (int i = 1; i < LEN; i++) {

        a.arr[i] = i;
        printordering(a);

        double alpha = (double)rand()/RAND_MAX;

        for(int beta = i-1; beta > 0; beta--) {
            
            
            
            //printf("%d\t%d\t%f\t%d\n",i,beta,alpha,a.len);


        }
    }
}

int main() {
    generateMallows(1.0);
    printf("hello");
};

