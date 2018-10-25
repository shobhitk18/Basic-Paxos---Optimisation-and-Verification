import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import shutil as util
import time

Analyze_folder = "Analysis"
final_file = 'final.csv'
analyze_file = 'temp.csv'
folder1 = "Output_Orig"
folder2 = "Output_Extended"
algorithms = ["orig.da", "orig_extended.da"]

def run():
	# Here we do multiple runs with varying values of r, d, w, tp and tl and report the observations in the form
	# of both csv and plots.
	for algo in algorithms:
		max_loss_rate = 1.0
		max_msg_delay = 1.0
		max_wait = 1.0
		num_points = 10

		p = 3
		a = 5
		l = 3
		n = 10
		r = 0.0
		d = 0.0
		w =  0.0
		tp = 1.0
		tl = 10.0
		
		if algo == "orig.da":
			Output_folder = "Output_Orig"
		elif algo == "orig_extended.da":
			Output_folder = "Output_Extended"

		# Lets vary the message loss rate now over multiple values keeping the rest same
		output_file = Output_folder + "/" + "loss_rate.csv"

		var = 0.0
		#title = ["Proposers: " + str(p), "Acceptor: " + str(a), "Learners: " + str(l),  "Message Delay: " + str(d), \
		#			"Wait Time: " + str(w), "Timeout(P): " + str(tp), "Timeout(L): " + str(tl)]

		output_heading = ['Loss Rate','Elapsed Time(Avg)', 'Elapsed Time(Std)' , 'Elapsed Time(Range)', 'CPU Time(Avg)', \
							'CPU Time(Std)', 'CPU Time(Range)', 'Timeout', 'Correctness']
		with open(output_file, mode='a') as file:
			writer = csv.writer(file)
			writer.writerow(output_heading)

		while var < max_loss_rate:
			r = var
			headings = ['Num Processes' , 'WallClock Time', 'Total_user_time', 'Total_system_time', 'Total_process_time', 'Total_memory', 'Timeout', 'Correctness']
			with open(analyze_file, mode='a') as file:
		             writer = csv.writer(file)
		             writer.writerow(headings)

			cmd = str('python -m da' + " " + algo + " " + str(p) + " " + str(a) + " " + str(l) + " "  + str(n) + " " + 
					str(r) + " " + str(d) + " " + str(w) + " " + str(tp) + " " + str(tl))
			os.system(cmd)
			print("Done Analyzing")
			df = pd.read_csv(analyze_file, nrows=None)

			isCorrect = 0 if df['Correctness'].sum() < n else 1
			isTimeout = 0 if df['Timeout'].sum() < n else 1
			elapsed_time_avg = df['WallClock Time'].mean()
			elapsed_std_dev = df['WallClock Time'].std()
			elapsed_time_range = df['WallClock Time'].max() - df['WallClock Time'].min()
			cpu_avg_time = df['Total_process_time'].mean()
			cpu_std_dev = df['Total_process_time'].std()
			cpu_time_range = df['Total_process_time'].max() - df['Total_process_time'].min()
			var = round(var,3)
			output_row = [var, round(elapsed_time_avg,3), elapsed_std_dev, elapsed_time_range, cpu_avg_time, cpu_std_dev , cpu_time_range, isTimeout, isCorrect]

			with open(output_file, mode='a') as file:
				writer = csv.writer(file)
				writer.writerow(output_row)

			del df
			analyze_file_cp = str(Analyze_folder + "/" + algo[:-3] + "_loss_rate" + "_" + str(time.clock()) + ".csv")
			print(analyze_file_cp)
			util.copyfile(analyze_file, analyze_file_cp)
			os.remove(analyze_file)
			var = var + max_loss_rate/num_points

		df = pd.read_csv(output_file, nrows=None)
		x = df['Loss Rate']
		y1 = df['Elapsed Time(Avg)']
		y2 = df['CPU Time(Avg)']
		
		fig, ax1 = plt.subplots(figsize=(20,10))
		ax1.plot(x, y1, 'b-')
		ax1.set_xlabel('Loss Rate')
		# Make the y-axis label, ticks and tick labels match the line color.
		ax1.set_ylabel('Elapsed Time(s)', color='b')
		ax1.tick_params('y', colors='b')

		ax2 = ax1.twinx()
		ax2.plot(x, y2, 'r--')
		ax2.set_ylabel('CPU Time(s)', color='r')
		ax2.tick_params('y', colors='r')
		fig.tight_layout()
		g_title = "Proposers: " + str(p), "Acceptor: " + str(a), "Learners: " + str(l),  "Message Delay: " + str(d), \
					"Wait Time: " + str(w), "Timeout(P): " + str(tp), "Timeout(L): " + str(tl)
		fig.suptitle(g_title, fontsize=16)
		fig_file = str(Output_folder + "/" + "loss_rate.png")
		fig.savefig(fig_file)
		plt.close(fig)
		# Resetting to original default value
		r = 0

		# Let's vary the message delay while keeping the rest of the values constant
		output_file = Output_folder + "/" + "msg_delay.csv"
		var = 0.0
		output_heading = ['Msg Delay(s)','Elapsed Time(Avg)', 'Elapsed Time(Std)' , 'Elapsed Time(Range)', 'CPU Time(Avg)', 'CPU Time(Std)',\
						 'CPU Time(Range)', 'Timeout', 'Correctness']
		with open(output_file, mode='a') as file:
			writer = csv.writer(file)
			writer.writerow(output_heading)
		while var < max_msg_delay:
			d = var
			headings = ['Num Processes' , 'WallClock Time', 'Total_user_time', 'Total_system_time', 'Total_process_time', 'Total_memory', 'Timeout', 'Correctness']
			with open(analyze_file, mode='a') as file:
		             writer = csv.writer(file)
		             writer.writerow(headings)

			cmd = str('python -m da' + " " + algo + " " + str(p) + " " + str(a) + " " + str(l) + " "  + str(n) + " " + 
					str(r) + " " + str(d) + " " + str(w) + " " + str(tp) + " " + str(tl))
			os.system(cmd)
			print("Done Analyzing")
			df = pd.read_csv(analyze_file, nrows=None)

			isCorrect = 0 if df['Correctness'].sum() < n else 1
			isTimeout = 0 if df['Timeout'].sum() < n else 1
			elapsed_time_avg = df['WallClock Time'].mean()
			elapsed_std_dev = df['WallClock Time'].std()
			elapsed_time_range = df['WallClock Time'].max() - df['WallClock Time'].min()
			cpu_avg_time = df['Total_process_time'].mean()
			cpu_std_dev = df['Total_process_time'].std()
			cpu_time_range = df['Total_process_time'].max() - df['Total_process_time'].min()
			var = round(var, 3)
			output_row = [var, elapsed_time_avg, elapsed_std_dev, elapsed_time_range, cpu_avg_time, cpu_std_dev , cpu_time_range , isTimeout, isCorrect]

			with open(output_file, mode='a') as file:
				writer = csv.writer(file)
				writer.writerow(output_row)

			del df
			analyze_file_cp = str(Analyze_folder + "/" + algo[:-3] + "_msg_delay" + "_" + str(time.clock()) + ".csv")
			print(analyze_file_cp)
			util.copyfile(analyze_file, analyze_file_cp)
			os.remove(analyze_file)
			var = var + max_msg_delay/num_points

		df = pd.read_csv(output_file, nrows=None)
		x = df['Msg Delay(s)']
		y1 = df['Elapsed Time(Avg)']
		y2 = df['CPU Time(Avg)']
		
		fig, ax1 = plt.subplots(figsize=(20,10))
		ax1.plot(x, y1, 'b-')
		ax1.set_xlabel('Msg Delay(s)')
		# Make the y-axis label, ticks and tick labels match the line color.
		ax1.set_ylabel('Elapsed Time(s)', color='b')
		ax1.tick_params('y', colors='b')

		ax2 = ax1.twinx()
		ax2.plot(x, y2, 'r--')
		ax2.set_ylabel('CPU Time(s)', color='r')
		ax2.tick_params('y', colors='r')
		fig.tight_layout()
		
		g_title = "Proposers: " + str(p), "Acceptor: " + str(a), "Learners: " + str(l),  "Loss Rate: " + str(r), \
					"Wait Time: " + str(w), "Timeout(P): " + str(tp), "Timeout(L): " + str(tl)

		fig.suptitle(g_title, fontsize=16)
		fig_file = str(Output_folder + "/" + "msg_delay.png")
		fig.savefig(fig_file)
		plt.close(fig)
		d = 0

		# Let's vary the delay over rounds while keeping the rest of the values constant
		output_file = Output_folder + "/" + "wait.csv"
		var = 0.0
		output_heading = ['Wait Time(s)','Elapsed Time(Avg)', 'Elapsed Time(Std)' , 'Elapsed Time(Range)', 'CPU Time(Avg)', 'CPU Time(Std)', \
							'CPU Time(Range)' , 'Timeout', 'Correctness']
		with open(output_file, mode='a') as file:
			writer = csv.writer(file)
			writer.writerow(output_heading)
		while var < max_wait:
			w = var
			headings = ['Num Processes' , 'WallClock Time', 'Total_user_time', 'Total_system_time', 'Total_process_time', 'Total_memory', 'Timeout', 'Correctness']
			with open(analyze_file, mode='a') as file:
		             writer = csv.writer(file)
		             writer.writerow(headings)

			cmd = str('python -m da' + " " + algo + " " + str(p) + " " + str(a) + " " + str(l) + " "  + str(n) + " " + 
					str(r) + " " + str(d) + " " + str(w) + " " + str(tp) + " " + str(tl))
			os.system(cmd)
			print("Done Analyzing")
			df = pd.read_csv(analyze_file, nrows=None)

			isCorrect = 0 if df['Correctness'].sum() < n else 1
			isTimeout = 0 if df['Timeout'].sum() < n else 1
			elapsed_time_avg = df['WallClock Time'].mean()
			elapsed_std_dev = df['WallClock Time'].std()
			elapsed_time_range = df['WallClock Time'].max() - df['WallClock Time'].min()
			cpu_avg_time = df['Total_process_time'].mean()
			cpu_std_dev = df['Total_process_time'].std()
			cpu_time_range = df['Total_process_time'].max() - df['Total_process_time'].min()
			var = round(var,3)
			output_row = [var, elapsed_time_avg, elapsed_std_dev, elapsed_time_range, cpu_avg_time, cpu_std_dev , cpu_time_range, isTimeout, isCorrect]

			with open(output_file, mode='a') as file:
				writer = csv.writer(file)
				writer.writerow(output_row)

			del df
			analyze_file_cp = str(Analyze_folder + "/" +  algo[:-3] +  "_wait" + "_" + str(time.clock()) + ".csv")
			print(analyze_file_cp)
			util.copyfile(analyze_file, analyze_file_cp)
			os.remove(analyze_file)
			var = var + max_wait/num_points
			
		df = pd.read_csv(output_file, nrows=None)
		x = df['Wait Time(s)']
		y1 = df['Elapsed Time(Avg)']
		y2 = df['CPU Time(Avg)']
		
		fig, ax1 = plt.subplots(figsize=(20,10))
		ax1.plot(x, y1, 'b-')
		ax1.set_xlabel('Wait Time(s)')
		# Make the y-axis label, ticks and tick labels match the line color.
		ax1.set_ylabel('Elapsed Time(s)', color='b')
		ax1.tick_params('y', colors='b')

		ax2 = ax1.twinx()
		ax2.plot(x, y2, 'r--')
		ax2.set_ylabel('CPU Time(s)', color='r')
		ax2.tick_params('y', colors='r')
		fig.tight_layout()

		g_title = "Proposers: " + str(p), "Acceptor: " + str(a), "Learners: " + str(l),  "Loss Rate: " + str(r), \
					"Msg Delay: " + str(d), "Timeout(P): " + str(tp), "Timeout(L): " + str(tl)

		fig.suptitle(g_title, fontsize=16)
		fig_file = str(Output_folder + "/" + "wait.png")
		fig.savefig(fig_file)
		plt.close(fig)
		w = 0

if __name__ == "__main__":
	if os.path.exists(Analyze_folder):
		util.rmtree(Analyze_folder)
	if os.path.exists(folder1):
		util.rmtree(folder1)
	if os.path.exists(folder2):
		util.rmtree(folder2)

	os.mkdir(Analyze_folder)
	os.mkdir(folder1)
	os.mkdir(folder2)

	if os.path.exists(final_file):
		os.remove(final_file)
	if os.path.exists(analyze_file):	
		os.remove(analyze_file)
	run()