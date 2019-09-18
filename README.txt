Project Description:

We will study optimizations of both Basic Paxos and Multi-Paxos. The goal is to better understand these algorithms.


1. Consider Basic Paxos as described using itemized steps by Lamport in his "Paxos made simple" paper.

(1) What liveness problems does the algorithm have? 

(2) What are possible methods for solving them?


2. Consider Multi-Paxos as described in pseudocode by van Renesse in his "Paxos made moderately complex" paper.

(1) What performance problems does the algorithm have? 

(2) What are possible methods for solving them?


3. Take the DistAlgo program for Lamport's Basis Paxos (under da/examples/lapaxos at http://github.com/DistAlgo/distalgo)

(1) Extend it into a version with preemption. You need to add correctness testing to check that executions with both the original and the extended versions are correct. There is no point to have a more live or faster program that is not correct.

(2) Measure the running times to learn a consensus value under varying values of 3 parameters: message loss rate, message delay, and wait time before a new round. You need to select the appropriate ranges of parameter values and their combinations to obtain interesting results.

Remember that, for performance evaluation, your measured results depend on the machine capacity you use. So do the ranges and combinations of parameter values.

Also, the running times (both elapsed time and total CPU time) should be averaged over a number of repeated runs. Here, you should report the range and standard deviation too because the variation is expected to be large.


Your program:

Your program must run under Python 3.6.5 or higher. Your main program must be named "main.da", and must run with a command like the following, where

"p", "a", "l" are the number of proposers, acceptors, and learners, respectively,
"n" is the number of repetitions for each run,
"r" is the message loss rate, between 0 for 0% loss and 1 for 100% loss,
"d" is the message delay, up to the number of seconds specified,
"w" is the wait time, in seconds, before trying a new round,
"tp" and "tl" are the timeout, in seconds, by proposers and learners, respectively, when timeout is used.

python.exe -m da main.da p a l n r d w tp tl

and do the following:

(1) run both versions of Basic Paxos;

(2) report the running times, ranges, and standard deviations, for each of them.

For selecting the argument values: "p", "a", "l" are usually 3, or occasionally 5; and "n" is better at least 10 or more.

You should specify several combinations and ranges of "r", "d", "w", "tp" and "tl", and report the resulting curves or trends for varying each of them. For example, you can provide a combination of all argument values where "r" varies over 5 different values. Generally, you want to vary the values of one parameter at a time.

You have the freedom to decide what additional information to report and what table and/or figure format to use.


Solution:

Project Directory: /

Source Files

1. controller.da:
	I have made use of the controller class to get the performance characteristics for my task
2. orig.da
	This file contains the original Basic Paxos implementation 
3. orig_extended.da
	This file contains the 'PreEmpt' implementation on top of Basic Paxos

4. run.py
	This file implements the testing code which runs various permutations of values for
	Loss rate, Message delays , Wait Delays, generates output files and plot graphs.User
	run the following command from inside the project directory to generate the outputs. 
	COMMAND: python run.py

Output:

There are two output folders:
1. Analyze: 
	This folder will contain the performance data for any particular combination over n iterations.
2. Output_Orig:
	The folder will contain the output data in the form of both csv file and graph which is averaged over n iterations
	Therefore it will contain entries like Avg , Standard Deviation and ranges. Along with Timeout and Correctness results
	In order to capture Timeout and correctness data for a batch of n iteration, I am keeping a threshold of 50% for both of
	them for reporting my
3. Output_Extended:
	This folder contains the output files and graphs for the runs done on orig_extended.da.

*******************************************************************************************
Note: PLEASE DON'T REMOVE THE FILE "temp.csv" GENERATED DURING THE RUN


#************************PREEMPT_CHANGE************************************

# Adding condition to break out of the await when receive a preempt with a proposal
# number value greater than the one on which the proposal is currently waiting to get
# a response
# Line 35:
     	elif some(received(('preempt',val), from_=a), has= val > n):
            n = val
# Getting the maximum proposal number which the acceptor has accepted and sending that
# proposal number back to the proposer with a 'preempt' tag
# Line 85:       
	else:
            preempt_n = max(setof(n2 , sent(('respond', n2, _))))
            send(('preempt', preempt_n), to =p)


#************************CORRECTNESS VERIFICATION***************************
# The decision about correctness is made on two criteria:
# 1. If there is a Timeout with any of the learner, then no learner should 
# learn any value.
# 2. In case of no Timeout with any of the learners, there should be a unique 
# value that must be learnt by all the learners.





********************************Observations**************************************
1.As the loss rate goes above 0.5 the system is mostly timing out due to not able to achieve consensus
The preempt allows the proposer to send another proposal without waiting for the timeout whereas the 
Orig code waits for the entire timeout duration which can one seen from the graph.

********************************************************************************************
References:
1.	https://github.com/DistAlgo/distalgo/blob/master/da/examples/lapaxos/orig.da
2.	https://arxiv.org/pdf/1704.00082.pdf
3.	https://github.com/DistAlgo/distalgo/tree/master/benchmarks/lapaxos					         	   
********************************************************************************************




***********************************************************EOF***********************************************************


