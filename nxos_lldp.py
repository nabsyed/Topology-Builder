import namecheck

def parser (data, current_node, cdp_nodes, file_append, output_links):
	
	lines = data.splitlines()
	first_line = 0
	
	for y in range (0,len(lines)):
		if "Device ID" in lines[y]:
			first_line = y
			break

	lengths = []
	final1 = []
	unique = []
	y = first_line

	while y < len(lines)-1:
#		if lines[y] ==  '\n':
		if len(lines[y]) <  2:
			y+=1
	
		delimited_line = lines[y].split()
		final1 = delimited_line
		
		if "." in final1[0] and "-" in final1[0]:					
			temp = final1[0]		
			final1[0] = final1[0][0:final1[0].index(".")]

			if "Eth" in final1[1]:
				pass
			else:
				final1[1] = "Eth" + temp.split("Eth",1)[1]				

		final2 = final1[:2] + final1[-1:]		
		final3 = current_node + "\t" + final2[0].lower() + "\t" + final2[1] + "\t" + final2[2] + "\n"

		if namecheck.namecheck(str(final2[0].lower())) is False:
			y+=1
			continue
			
		if ((final2[0].lower() != current_node.lower()) and 
			(final2[0].lower() not in unique) and 
			(final2[0].lower() not in cdp_nodes)):
			
			unique.append (final2[0].lower())		
		
		if final2[0].lower() not in cdp_nodes:
			output_links.put(final3)
		
		y+=1
		
	return unique