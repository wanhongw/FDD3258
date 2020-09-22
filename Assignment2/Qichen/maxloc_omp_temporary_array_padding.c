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

typedef struct 
{
    double val; int loc; char pad[128];
} tvals;


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
    
    #pragma omp parallel shared(maxinfo)
    {
        int id = omp_get_team_num();
        maxinfo[id].val = -1.0e30;
        #pragma omp parallel for
            for (int i=0; i < 1000000; i++){
            if (x[i] > maxinfo[id].val){
                maxinfo[id].loc = i;
                maxinfo[id].val = x[i];
            } 

        }
    }

    
    tEnd = mysecond();
    t =  tEnd - tStart;
    printf( "%f\n",t);

}


