import namecheck

def parser (data, current_node, file_append, output_links):
	
	lines = data.splitlines()
	first_line = 0

	for y in range (0,len(lines)):
		if "Port" in lines[y]:
			first_line = y
			break

	links_file = open ('data/links-%s.txt' %file_append, 'a')

	lengths = []
	final1 = []
	unique = []
	y = first_line + 1

	while y < len(lines):
		delimited_line = lines[y].split()
		final1 = delimited_line
		
		if "." in final1[1]:
			final1[1] = final1[1][0:(final1[1].index("."))]

		final2 = final1[:3]				
		final3 = current_node + "\t" + final2[1].lower() + "\t" + final2[0] + "\t" + final2[2] + "\n"
		
		if namecheck.namecheck(str(final2[1].lower())) is False:
			y+=1
			continue			
			
		output_links.put(final3)

		if (final2[1].lower() != current_node.lower()) and (final2[1].lower() not in unique):
			unique.append (final2[1].lower())					

		y+=1
		
	return unique