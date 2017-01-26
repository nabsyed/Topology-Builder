import pydot
import layers
import node_sort
import hlink_detect

def plot (upper_limit,lower_limit, location_code, file_append, interface_labels, graph_type):

	with open ('data/links_scoped-%s.txt' %file_append, 'r') as links_file:
		lines = links_file.readlines()

	g1 = pydot.Dot (graph_type = 'graph', splines=graph_type, ranksep="6.0", nodesep="0.3")

	for j in range (0, len(lines)):
		delimited = lines[j].split()
		
		device_type_1 = delimited[0][delimited[0].find("-") + 1 : delimited[0].find("-") + 3]			
		device_type_2 = delimited[1][delimited[1].find("-") + 1 : delimited[1].find("-") + 3]

		if (int(layers.layers_dict(device_type_1)) < int(layers.layers_dict(upper_limit))) or (int(layers.layers_dict(device_type_2)) < int(layers.layers_dict(upper_limit))):
			continue

		if (int(layers.layers_dict(device_type_1)) > int(layers.layers_dict(lower_limit))) or (int(layers.layers_dict(device_type_2)) > int(layers.layers_dict(lower_limit))):
			continue

		if interface_labels is 'y':
			t_label=str(delimited[2])
			h_label=str(delimited[3])
		else:
			t_label=' '
			h_label=' '
			
		edge = pydot.Edge (str(delimited[0]), str(delimited[1]),
							color="black",
							fontsize='10',
							minlen="2.5",
							penwidth="1.0",
							labeldistance="1.2",
							taillabel=t_label,
							headlabel=h_label)
		g1.add_edge (edge)

	nodes = node_sort.node_sort(upper_limit,lower_limit, location_code, file_append)

	layer = pydot.Subgraph(rank='same')
	h_node = hlink_detect.hlink_detect(upper_limit,lower_limit, location_code, file_append)

	for i in range (0, len(nodes)):
		layers_key = layers.layers_key()[i]	
		list = nodes[str(layers_key)]
			
		if len(list) != 0:
		
			if (layers_key == 'ec'):
				v_shape="box3d"
				v_width="3.0"
				v_height="2.0"
				v_penwidth="1.1"
				v_style="rounded, filled, bold"
				v_align="center"
				v_fontsize="20.0"
				v_fontname="arial"
			elif (layers_key == 'ed'):
				v_shape="box3d"
				v_width="3.0"
				v_height="2.0"
				v_penwidth="1.1"
				v_style="rounded, filled, bold"
				v_align="center"
				v_fontsize="20.0"
				v_fontname="arial"		
			elif (layers_key == 'a1') or (layers_key == 'a2'):
				v_shape="box3d"
				v_width="1.0"
				v_height="0.5"
				v_penwidth="0.8"
				v_style="rounded, filled, bold"
				v_align="center"
				v_fontsize="12.0"
				v_fontname="arial"
			else:
				v_shape="box3d"
				v_width="3.0"
				v_height="2.0"
				v_penwidth="1.1"
				v_style="rounded, filled, bold"
				v_align="center"
				v_fontsize="20.0"
				v_fontname="arial"


			for k in range (0, len(list)):
				node = pydot.Node(str(list[k]),
								shape=v_shape,
								width=v_width,
								height=v_height,
								penwidth=v_penwidth,
								style=v_style,
								align=v_align,
								fontsize=v_fontsize,
								fontname=v_fontname)
				layer.add_node(node)
		
		g1.add_subgraph(layer)

		layer = pydot.Subgraph(rank='same')
		
		if len(list) != 0:
			for k in range (0, len(list)-1):
				if list[k] not in h_node:	
	
					edge = pydot.Edge (str(list[k]), 
						str(list[k+1]),	
						minlen="1.0",						
						style='invis')
					g1.add_edge (edge)

	g1.write_svg('img/topology-%s.svg' %file_append)