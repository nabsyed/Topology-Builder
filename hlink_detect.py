import layers
import node_sort
import time

def hlink_detect (upper_limit, lower_limit, location_code, file_append):

	with open ('data/links_scoped-%s.txt' %file_append, 'r') as links_file:
		lines = links_file.readlines()

	h_node = []							
	k1 = 0
	k2 = 0
	current_line_k1 = 0
	current_line_k2 = 0
	both_found = 0
	first_match = False					
	
	nodes = node_sort.node_sort(upper_limit, lower_limit, location_code, file_append)		
	
	for i in range (0, len(nodes)):
			
		layers_key = layers.layers_key()[i]					
		temp_list = nodes[str(layers_key)]
		
		if len(temp_list) != 0:
			for m in range (0, len(lines)):
				delimited = lines[m].split()
				
				if delimited[0] in temp_list:
					k1 = temp_list.index(delimited[0])
					current_line_k1 = m
				if delimited[1] in temp_list:
					k2 = temp_list.index(delimited[1])
					current_line_k2 = m					
				
				if k2-k1 == 1 and current_line_k1 == current_line_k2 and first_match == False:
					first_match = True			
					
					if (temp_list.index(delimited[0]) not in h_node) and (temp_list.index(delimited[1]) not in h_node):
						h_node.append (delimited[0])		

				first_match = False
				k1 = 9999999
				k2 = 9999999

	return h_node