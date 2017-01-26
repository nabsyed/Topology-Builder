import discover
import info
import layers
import link_sort
import multiprocessing as mp
import node_sort
import plot_small
import sys
import time


def links_writer(output_links):
	with open ('data/links-%s.txt' %file_append, 'a') as links_file:
		while True:
			text = str(output_links.get())
			if text != 'end_crawl':
				links_file.write(text)
			else:
				break


def next_access(new_add, output_nodes, output_links):
	global count
	count+=1
	next_nodes = []
#	print "\nnew_add from next_access:", new_add, "(%d)" %count
	
	for i in range (0,len(new_add)):
		if new_add[i] not in nodes:
			nodes.append(new_add[i])
			next_nodes.append(new_add[i])

	if len(next_nodes) > 0:
		multi_access(next_nodes, output_nodes, output_links)


def multi_access(next_nodes, output_nodes, output_links):
	global count

	count+=1
	processes = []
	filtered_next_nodes = []

#	print "\n\nNodes from multi_access:", nodes
#	print "\n\tnext_nodes from multi_access:", next_nodes, "(%d)" %count

	# Empty queue if not already empty
	while not output_nodes.empty():
		output_nodes.get()
		
	for i in range (len(next_nodes)):
		node_device_type = next_nodes[i][next_nodes[i].find("-") + 1 : next_nodes[i].find("-") + 3]
		node_location_code = next_nodes[i][0:len(location_code)]
	
		if (node_location_code != location_code) and (location_code != 'all'):
			continue
		if layers.layers_dict(node_device_type) == None:
			print "Node type not found,", next_nodes[i]
			continue
		
#		print "\n\tnext_nodes from multi_access:", next_nodes[i]
		if (int(layers.layers_dict(node_device_type)) >= int(layers.layers_dict(upper_limit)) and int(layers.layers_dict(node_device_type)) <= int(layers.layers_dict(lower_limit))):
			filtered_next_nodes.append(next_nodes[i])

	for i in range (len(filtered_next_nodes)):
		process = mp.Process(target=discover.get_ndp_output, args=(filtered_next_nodes[i],username,password,file_append,output_nodes,output_links))
		process.daemon=True
		processes.append(process)
		all_processes.append(process)

	text_display = "\r" + str(len(nodes)) + " devices found"
	sys.stdout.write(text_display)
	sys.stdout.flush()
	
	i=0
	for p in processes:
#		print filtered_next_nodes[i], p.name, "starting"
		p.start()
		i+=1

	# get process results from the output queue
	results = [output_nodes.get() for p in processes]
	
	for j in range (0,len(results)):
#		print "\n\nResults:", j, results[j], len(results), len(results[j])
		if len(results[j]) > 0:
			next_access(results[j],output_nodes,output_links)

	text_display = "\r" + str(len(nodes)) + " devices found"
	sys.stdout.write(text_display)
	sys.stdout.flush()


def main():
	output_nodes = mp.Queue()
	output_links = mp.Queue()

	script_start_time = time.time()												# Start time

	#----------------------------------------------------------------				
	process = mp.Process(target=links_writer, args=(output_links,))				# Spawn 'links_writer' process
	#process.daemon = True											# If this process is daemon, writing to file doesn't work
	process.start()
		
	print "\n"
	#----------------------------------------------------------------				
	next_access([seed_device], output_nodes, output_links)	# Start crawl from seed device

	i = 0
#	print "\nTotal # of processes:", len(all_processes)
	while i < len (all_processes):									# Ensure all processes have shut down
#		print "process number", i, all_processes[i].is_alive()
		if all_processes[i].is_alive() == False:
			i+=1
	
	output_links.put('end_crawl')									# End crawl: signal to 'links_writer' to release file
	#----------------------------------------------------------------				

	with open ('data/nodes-%s.txt' %file_append, 'a') as nodes_file:
		for i in range (0, len(nodes)):
			nodes_file.write(nodes[i] + "\n")

	nodes_dict = node_sort.node_sort(upper_limit,lower_limit, location_code, file_append)
	
	lengths = [len(v) for v in nodes_dict.values()]
	for i in nodes_dict:
		for j in nodes_dict[i]:
			nodes_discovered.append(j)			

	print "\n\n", len(nodes_discovered), "nodes discovered:", ', '.join(nodes_discovered), "\n\n"
	
	#----------------------------------------------------------------			
	print "Sorting links..."
	link_sort.link_sort(upper_limit, lower_limit, location_code, file_append)
	#----------------------------------------------------------------			
	data_time = time.time() - script_start_time
	#----------------------------------------------------------------			
	print "Plotting..."
	plot_time_start = time.time()
	plot_small.plot(upper_limit, lower_limit, location_code, file_append, interface_labels, graph_type)
	plot_time = time.time() - plot_time_start
	#----------------------------------------------------------------			

	exec_time = time.time() - script_start_time

	print ("\nData Collection and Analysis time: \t%0.2f seconds") % data_time
	print ("Plotting time: \t\t\t\t%0.2f seconds") % plot_time
	print ("Total Execution time: \t\t\t%0.2f seconds\n") % exec_time

	print "Topology generated at:" %file_append


if __name__ == '__main__':
	info.banner()                                                          
	seed_device = info.seed_device()
	upper_limit = info.upper_limit()
	lower_limit = info.lower_limit(upper_limit)
	location_code = info.location_code()
	graph_type = info.graph_type()
	interface_labels = 'n'
	username, password, max_auth_tries = info.auth_check(seed_device)

	if max_auth_tries is True:
		print "\nAuthentication failed after 3 attempts. Exiting...\n"
		sys.exit()

	file_seed_time = (time.strftime("%Y%m%d-%H%M%S"))
	file_append = username + "-" + file_seed_time
	nodes = []
	nodes_discovered = []
	all_processes = []
	count = 0

	main()
