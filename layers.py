def layers_dict (string):

	layers_dict = {  '1':['top'],
					 '2':['core'],
					 '3':['distribution'],
					 '4':['access'],
					 '5':['bottom']}
					
	for i in layers_dict:
		for j in layers_dict[i]:
			if string in j:
				return i
				
				
def layers_list ():
	
	layers_list = [ 'top'
					'core',
					'distribution',
					'access',
					'bottom']

	return layers_list
	
	
def layers_order ():
	
	layers_order = [1,
					2,
					3,
					4,
					5]

	return layers_order
	
	
def layers_key ():
	
	layers_key = [  'top'
					'core',
					'distribution',
					'access',
					'bottom']

	return layers_key

	
def nodes_dict ():
		
	nodes_dict = {'top':[], 
				  'core':[], 
				  'distribution':[],
				  'access':[],
				  'bottom':[]}
	
return nodes_dict