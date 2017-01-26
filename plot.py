import pydot
import layers
import node_sort
import hlink_detect
def plot (upper_limit, lower_limit, location_code, file_append):
	
	with open ('data/links_sorted-%s.txt' %file_append, 'r') as links_file:
		lines = links_file.readlines()
	
	g1 = pydot.Dot (graph_type = 'graph', splines='spline', ranksep="8.5", nodesep="0.01")		
	
	for j in range (0, len(lines)):
		delimited = lines[j].split()
		device_type_1 = delimited[0][delimited[0].find("-") + 1 : delimited[0].find("-") + 3]			
		device_type_2 = delimited[1][delimited[1].find("-") + 1 : delimited[1].find("-") + 3]
		
		if (int(layers.layers_dict(device_type_1)) < int(layers.layers_dict(upper_limit))) or (int(layers.layers_dict(device_type_2)) < int(layers.layers_dict(upper_limit))):
			continue
		
		if (int(layers.layers_dict(device_type_1)) > int(layers.layers_dict(lower_limit))) or (int(layers.layers_dict(device_type_2)) > int(layers.layers_dict(lower_limit))):
			continue
		
		edge = pydot.Edge (str(delimited[0]), str(delimited[1]),
							color="black",
							fontsize='10',
							minlen="3.0",
							penwidth="0.4",
							labeldistance="1.2")
		g1.add_edge (edge)
	nodes = node_sort.node_sort(upper_limit, lower_limit, location_code)
	
	layer = pydot.Subgraph(rank='same')
	h_node = hlink_detect.hlink_detect(upper_limit, lower_limit, location_code, file_append)
	
	for i in range (0, len(nodes)):
		layers_key = layers.layers_key()[i]					
		list = nodes[str(layers_key)]

		if len(list) != 0:
			if (layers_key == 'br') or (layers_key == 'xr'):
				for k in range (0, len(list)):
					node = pydot.Node(str(list[k]),
									shape="record",
									width="15.0",
									height="4.0",
									penwidth="10.0",
									style="rounded, filled, bold",
									align="center",
									fontsize="120.0",
									fontname="arial")
					layer.add_node(node)
			elif (layers_key == 'ar'):
				for k in range (0, len(list)):
					node = pydot.Node(str(list[k]),
									shape="oval",
									width="10.0",
									height="2.5",
									penwidth="10.0",
									style="rounded, filled, bold",
									align="center",
									fontsize="100.0",
									fontname="arial")
					layer.add_node(node)
			elif (layers_key == 'ec'):
				for k in range (0, len(list)):
					node = pydot.Node(str(list[k]),
									shape="record",
									width="10.0",
									height="2.5",
									penwidth="10.0",
									style="rounded, filled, bold",
									align="center",
									fontsize="100.0",
									fontname="arial")
					layer.add_node(node)
			elif (layers_key == 'ed'):
				for k in range (0, len(list)):
					node = pydot.Node(str(list[k]),
									shape="record",
									width="4.5",
									height="2.0",
									penwidth="2.0",
									style="rounded, filled, bold",
									align="center",
									fontsize="40.0",
									fontname="arial")
					layer.add_node(node)
			elif (layers_key == 'a1') or (layers_key == 'a2'):
				for k in range (0, len(list)):
					node = pydot.Node(str(list[k]),
									shape="record",
									width="0.1",
									height="0.1",
									penwidth="3.0",
									color="white",
									style="rounded, filled, bold",
									align="center",
									fontsize="5.0",
									fontname="arial")
					layer.add_node(node)
			else:
				for k in range (0, len(list)):
					node = pydot.Node(str(list[k]),
									shape="record",
									width="10.0",
									height="2.5",
									penwidth="10.0",
									style="rounded, filled, bold",
									align="center",
									fontsize="100.0",
									fontname="arial")
					layer.add_node(node)			
		
		g1.add_subgraph(layer)
		
		layer = pydot.Subgraph(rank='same')
		
		if len(list) != 0:
			for k in range (0, len(list)-1):
				if list[k] not in h_node:	
					edge = pydot.Edge (str(list[k]), 
						str(list[k+1]),	
						minlen="2.0",						
						style='invis')
					g1.add_edge (edge)					
	
	g1.write_svg('img/topology-%s.svg' %file_append)					