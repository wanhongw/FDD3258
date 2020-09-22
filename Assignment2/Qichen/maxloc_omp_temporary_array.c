#include "stdio.h"
#include "stdlib.h"
#include <string.h>
#include <sys/time.h>
#include "omp.h"
// timer
double mysecond(){
struct timeval tp;
struct timezone tzp;
int i;
i = gettimeofday(&tp,&tzp);
return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
}

void main()
{

    double tStart, tEnd;
    double x[1000000],t;
    int MAX_THREADS = 16;
    tStart = mysecond();

    srand(time(0)); // seed
    #pragma omp parallel for
        for(int i=0; i < 1000000;i++){
            // Generate random number between 0 and 1
            x[i] = ((double)(rand()) / RAND_MAX)*((double)(rand()) / RAND_MAX)*((double)(rand()) / RAND_MAX)*1000;
        }

    int maxloc[MAX_THREADS],molc;
    double maxval[MAX_THREADS],mval;
    #pragma omp parallel shared(maxval,maxloc)
    {
        int id = omp_get_team_num();
        maxval[id]=-1.0e30;
        #pragma omp for
            for (int i=0; i < 1000000; i++){
            if (x[i] > maxval[id]){
                maxloc[id] = i;
                maxval[id] = x[i];
            } 

        }
    }

    
    tEnd = mysecond();
    t =  tEnd - tStart;
    printf( "%f\n",t);

}


