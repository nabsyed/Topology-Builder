from operator import itemgetter
import layers
import node_sort
import fileinput

def link_sort(upper_limit, lower_limit, location_code, file_append):
	with open ('data/links-%s.txt' %file_append, 'r') as links_file:
		lines = links_file.readlines()
	
	# Sorted by first column and de-duped
	sorted_file = open ('data/links_sorted-%s.txt' %file_append, 'a')
	sorted_file.seek(0)
	sorted_file.truncate()
	
	sorted_list = []
	counted = []

	for i in range (0, len(lines)):
		delimited = lines[i].split()
		sorted_list.append(delimited)
#		first_column.append(sorted_list[i][0])

#	first_column_unique = list(set(first_column))			# Make first column unique

	sorted_list.sort(key=itemgetter(0))						# Sort table by first column

	# Remove duplicates
	for i in range (0, len(sorted_list)):
		if sorted_list[i][0] not in counted:
			counted.append(sorted_list[i][0])
			
		if sorted_list[i][0] == sorted_list[i][1]:			# Keep loopback link
			sorted_file.write('\t'.join(sorted_list[i])+"\n")
			continue

		if sorted_list[i][1] in counted:
			continue
		else:
			sorted_file.write('\t'.join(sorted_list[i])+"\n")

	sorted_file.close()			

	link_scope(upper_limit, lower_limit, location_code, file_append)


def link_scope(upper_limit, lower_limit, location_code, file_append):
	with open ('data/links_sorted-%s.txt' %file_append, 'r') as links_file:
		lines = links_file.readlines()
		
	scoped_file = open ('data/links_scoped-%s.txt' %file_append, 'a')
	scoped_file.seek(0)
	scoped_file.truncate()
	
	nodes = node_sort.node_sort(upper_limit, lower_limit, location_code, file_append)
	
	both_found = 0
	k1 = 0
	k2 = 0

	for i in range (0, len(lines)):
		delimited = lines[i].split()
		device_type_1 = delimited[0][delimited[0].find("-") + 1 : delimited[0].find("-") + 3]
		device_type_2 = delimited[1][delimited[1].find("-") + 1 : delimited[1].find("-") + 3]
		node_location_code_1 = delimited[0][0:len(location_code)]
		node_location_code_2 = delimited[1][0:len(location_code)]
		
		if location_code != 'all':
			if (node_location_code_1 != location_code) or (node_location_code_2 != location_code):
				continue

		if ((int(layers.layers_dict(device_type_1)) < int(layers.layers_dict(upper_limit))) or (int(layers.layers_dict(device_type_2)) < int(layers.layers_dict(upper_limit)))):
			continue

		if ((int(layers.layers_dict(device_type_1)) > int(layers.layers_dict(lower_limit))) or (int(layers.layers_dict(device_type_2)) > int(layers.layers_dict(lower_limit)))):
			continue

		if int(layers.layers_dict(device_type_1)) < int(layers.layers_dict(device_type_2)):
			new_delimited = delimited[0] + "\t" + delimited[1] + "\t" + delimited[2] + "\t" + delimited[3] + "\n"
			scoped_file.write(new_delimited)
		
		elif int(layers.layers_dict(device_type_1)) > int(layers.layers_dict(device_type_2)):
			new_delimited = delimited[1] + "\t" + delimited[0] + "\t" + delimited[3] + "\t" + delimited[2] + "\n"
			scoped_file.write(new_delimited)

		elif int(layers.layers_dict(device_type_1)) == int(layers.layers_dict(device_type_2)):

			for key in nodes.keys():
				if delimited[0] in nodes[key]:
					k1 = nodes[key].index(delimited[0])
					both_found+=1
				if delimited[1] in nodes[key]:
					k2 = nodes[key].index(delimited[1])
					both_found+=1
				if both_found is 2:
					both_found = 0
					break
			
			if k1 < k2:
				new_delimited = delimited[0] + "\t" + delimited[1] + "\t" + delimited[2] + "\t" + delimited[3] + "\n"
				scoped_file.write(new_delimited)
			elif k1 > k2:
				new_delimited = delimited[1] + "\t" + delimited[0] + "\t" + delimited[3] + "\t" + delimited[2] + "\n"
				scoped_file.write(new_delimited)
	
	scoped_file.close()
	
	for line in fileinput.FileInput('data/links_scoped-%s.txt' %file_append, inplace=1):
		line = line.replace(":","-")
		print line,