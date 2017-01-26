import natsort
import layers
import time

def node_sort(upper_limit, lower_limit, location_code, file_append):

	with open ('data/nodes-%s.txt' %file_append, 'r') as nodes_file:
		devices = nodes_file.read().splitlines() 					
		
	nodes_dict = layers.nodes_dict()
 	layers_key = layers.layers_key()

	for i in range (0, len(devices)):
		device_type = devices[i][devices[i].find("-") + 1 : devices[i].find("-") + 3]
		node_location_code = devices[i][0:len(location_code)]
	
		if device_type in ['ma','lc','ic','sc']:
			device_type = 'cc'
		elif device_type in ['ra','ea','ha']:
			device_type = 'a1'	
		elif device_type in ['la','da','sa','ia']:
			device_type = 'a2'
		elif device_type not in layers.layers_list():
			print "Device Type '%s' not found" %device_type
			continue
		
		if (node_location_code != location_code) and (location_code != 'all'):
			continue
		elif (int(layers.layers_dict(device_type)) < int(layers.layers_dict(upper_limit))) or (int(layers.layers_dict(device_type)) > int(layers.layers_dict(lower_limit))):
			continue
		else:
			nodes_dict[device_type].append(devices[i])			
	
	for i in nodes_dict:
		for j in nodes_dict[i]:
			nodes_dict[i] = natsort.natsorted(nodes_dict[i])


	return nodes_dict