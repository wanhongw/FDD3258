import os
import matplotlib.pyplot as plt

'''
Qichen Xu 2020, KTH.
Questions. Here the steps you need to follow for the exercise submission:

1.Run the STREAM benchmark for 5 times and record the average values of bandwidth and its standard deviation for the copy kernel
Prepare a plot (with Excel, Matlab, Gnuplot, …) comparing the bandwidth using 1-2-4-8-12-16-20-24-28-32 threads.

2.How does the bandwidth measured with copy kernel depend on the number of threads?

3.Prepare a plot comparing the bandwidth measured with copy kernel with static, dynamic and guided schedules using 32 threads.
How do you set the schedule in the STREAM code? What is the fastest schedule and why do you think it is so?
'''

#Solve the first problem
#compile the C++ stream.c with flag :-O -fopenmp
compile_stream_c = os.system("gcc-9 -O -fopenmp stream.c -o stream")
#run and record the average kernel copy



#uncomment if on laptop
#threads_number = [1,2,4,8,12,16]
#uncomment if on HPC
threads_number = [1,2,4,8,12,16,20,24,28,32]
copy_kernel_result_average = []

for tn in threads_number:
    copy_kernel_result = 0
    os.system("export OMP_NUM_THREADS={}".format(tn))
    for step in range(5):
        os.system("./stream > log")
        with open(r"./log", 'r') as file: 
            for line in file.readlines(): 
                if "Copy:" in line: 
                    s = line.split() 
                    copy_kernel_result = copy_kernel_result + float(s[1])
        os.system('rm log')
    average = copy_kernel_result/5       
    copy_kernel_result_average.append(average)


#plot the bandwidth
fig, ax = plt.subplots()
ax.plot(threads_number, copy_kernel_result_average)
ax.set(xlabel='thread number', ylabel='bandwidth MB/s',
       title='STREAM benchmark---Copy bandwidth')
ax.grid()
fig.savefig("STREAM_benchmark_Copy_bandwidth.png")







#Solve the thrid problem
#compile with static and dynamic, stream.c is in guided model
compile_stream_c = os.system("gcc-9 -O -fopenmp stream_static.c -o stream_static")
compile_stream_c = os.system("gcc-9 -O -fopenmp stream_dynamic.c -o stream_dynamic")

#run and record the average kernel copy
tn = 32
schedule_list = ["stream","stream_static","stream_dynamic"]

copy_kernel_result_average = []
for schedule in schedule_list:
    copy_kernel_result = 0
    os.system("export OMP_NUM_THREADS={}".format(tn))
    for step in range(5):
        os.system("./{} > log".format(schedule))
        with open(r"./log", 'r') as file: 
            for line in file.readlines(): 
                if "Copy:" in line: 
                    s = line.split() 
                    copy_kernel_result = copy_kernel_result + float(s[1])
        os.system('rm log')
    average = copy_kernel_result/5       
    copy_kernel_result_average.append(average)


#plot the bandwidth
fig, ax = plt.subplots()
ax.plot(schedule_list, copy_kernel_result_average)
ax.set(xlabel='schedule name', ylabel='bandwidth MB/s',
       title='STREAM benchmark---Copy bandwidth---different schedule')
ax.grid()
fig.savefig("STREAM_benchmark_Copy_bandwidth_different_schedule.png")
    
