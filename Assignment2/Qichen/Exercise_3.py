
"""
qichen xu

1.Measure the performance of the serial code (average + standard deviation)

2.Use omp parallel for construct to parallelize. Run the code with 32 threads 
and measure the execution time (average + standard deviation). Is the code correct? If not, why so?

3.Use omp critical  to protect the code region that might be updated by multiple
 threads concurrently. Measure the execution time for both versions (omp critical) 
 varying the number of threads: 1,2,4,8,16, 20, 24, 28 and 32. How does the performance
  compare to 1 and 2? What is the reason for the performance gain/loss?

4.Try to avoid the use of critical section. Let each thread find the maxloc 
in its own data then combine their local result to get the final result. For 
instance, we can use temporary arrays indexed by thread number to hold the values 
found by each thread:
Measure the performance of the new implementation varying the number of threads: 
    1,2,4,8,16, 20, 24, 28 and 32. Does the performance increase as expected? If not why?

5.Write a version of the code in 4 using a technique to remove false sharing 
with padding. Measure the performance of code varying the number of threads: 
    1,2,4,8,16, 20, 24, 28 and 32.
"""
import os
import numpy as np
import matplotlib.pyplot as plt


#solve the question 1
#Average in 10 times
os.system("gcc maxloc.c -o maxloc")
ex_time = []
total_time= 0

for step in range(10):
    os.system("./{} >> log".format("maxloc"))
with open(r"./log", 'r') as file: 
    for line in file.readlines():
        ex_time.append(line)
        total_time = total_time+ float(line)
average = total_time/10
standard_deviation = np.std(np.asarray(ex_time, dtype=np.float32))
os.system("rm log")
print("the standard deviation is : {}, average execution time is {}:".format(standard_deviation,average))



#solve the question2
#uncomment blew on HPC
#tn = 32  
tn = 16
os.system("gcc-9 -fopenmp maxloc_omp.c -o maxloc_omp")

os.system("export OMP_NUM_THREADS={}".format(tn))

for step in range(10):
    os.system("./{} >> log".format("maxloc_omp"))
with open(r"./log", 'r') as file: 
    for line in file.readlines():
        ex_time.append(line)
        total_time = total_time+ float(line)
average = total_time/10
standard_deviation = np.std(np.asarray(ex_time, dtype=np.float32))
os.system("rm log")
print("the standard deviation with omp is : {}, average execution time with omp is {}:".format(standard_deviation,average))



#solve the question 3

tn = ["1","2","4","8","16"]
#uncomment blew on HPC
#tn = [1,2,4,8,16,20,24,28,32]
os.system("gcc-9 -fopenmp maxloc_omp_critical.c -o maxloc_omp_critical")

for i in tn:
    os.system("export OMP_NUM_THREADS={}".format(i))
    for step in range(10):
        os.system("./{} >> log".format("maxloc_omp_critical"))
    with open(r"./log", 'r') as file: 
        for line in file.readlines():
            ex_time.append(line)
            total_time = total_time+ float(line)
    average = total_time/10
    standard_deviation = np.std(np.asarray(ex_time, dtype=np.float32))
    os.system("rm log")
    print("the standard deviation with omp and critical protect with {tr} threads is : {sd}, average execution time with omp critical protect with {tr} threads is {av}:".format(tr = i,sd = standard_deviation,av = average))
    


#solve the question 4


tn = ["1","2","4","8","16"]
#uncomment blew on HPC
#tn = [1,2,4,8,16,20,24,28,32]
os.system("gcc-9 -fopenmp maxloc_omp_temporary_array.c -o maxloc_omp_temporary_array")

for i in tn:
    os.system("export OMP_NUM_THREADS={}".format(i))
    for step in range(10):
        os.system("./{} >> log".format("maxloc_omp_temporary_array"))
    with open(r"./log", 'r') as file: 
        for line in file.readlines():
            ex_time.append(line)
            total_time = total_time+ float(line)
    average = total_time/10
    standard_deviation = np.std(np.asarray(ex_time, dtype=np.float32))
    os.system("rm log")
    print("the standard deviation with omp and temporary array with {tr} threads is : {sd}, average execution time with omp temporary array with {tr} threads is {av}:".format(tr = i,sd = standard_deviation,av = average))
 

#solve the question 5

#not work now.

