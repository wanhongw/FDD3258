import os
import matplotlib.pyplot as plt
import numpy as np
#Solve the problem 2
#compile the C++ stream.c with flag :-O -fopenmp
compile_stream_c = os.system("gcc-9 -Wall -O2 -fopenmp -o DFTW DFTW_1.c")
#run and record the average kernel copy



#uncomment if on laptop
threads_number = [16]
#uncomment if on HPC
#threads_number = [32]
DFT_time = []

for tn in threads_number:
    DFT_time_for_average = 0
    os.system("export OMP_NUM_THREADS={}".format(tn))
    for step in range(10):
        os.system("./DFTW > log")
        with open(r"./log", 'r') as file: 
            for line in file.readlines(): 
                if "DFTW computation in" in line: 
                    s = line.rstrip("seconds\n")
                    s = s.lstrip("DFTW computation in")
                    s = s.split()
                    DFT_time_for_average = DFT_time_for_average + float(s[0])
                    DFT_time.append(float(s[0]))
        os.system('rm log')
    average = DFT_time_for_average/10      
    standard_deviation = np.std(np.asarray(DFT_time, dtype=np.float32))
print("run 10 times and average values is {}, standard deviation is {}".format(average,standard_deviation))







#uncomment if on laptop
threads_number = [16,14,12,10,8,6,4,2,1]
#uncomment if on HPC
#threads_number = [1,2,4,6,8,12,14,16,18,20,24,28,32]
average_ex_time = []

for tn in threads_number:
    DFT_time = []
    DFT_time_for_average = 0
    os.system("export OMP_NUM_THREADS={}".format(tn))
    os.system("echo $OMP_NUM_THREADS")
    for step in range(10):
        os.system("./DFTW > log")
        with open(r"./log", 'r') as file: 
            for line in file.readlines(): 
                if "DFTW computation in" in line: 
                    s = line.rstrip("seconds\n")
                    s = s.lstrip("DFTW computation in")
                    s = s.split()
                    DFT_time_for_average = DFT_time_for_average + float(s[0])
                    DFT_time.append(float(s[0]))
        os.system('rm log')
    average = DFT_time_for_average/10      
    average_ex_time.append(average)

        
#plot the bandwidth
fig, ax = plt.subplots()
ax.plot(threads_number, average_ex_time)
ax.set(xlabel='thread number', ylabel='average_ex_time /s',
       title='thread number to average_ex_time')
ax.grid()
fig.savefig("exercise4.png")# -*- coding: utf-8 -*-

