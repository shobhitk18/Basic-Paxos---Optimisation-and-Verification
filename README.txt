
						ASSIGNMENT No. 4(CSE-535)
						Due : 22nd October
		
SUBMISSION DETAILS:					 
	Name : Shobhit Khandelwal
	SBU ID: 112074908


BRIEF:

Project Directory:

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


