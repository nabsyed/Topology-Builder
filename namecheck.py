import layers

names = layers.layers_list()

def namecheck (hostname):
	valid = False

	if hostname.count('-') > 1:
		return valid

	for j in range (0,len(names)):
		if ("-" + names[j]) in hostname:
			valid = True
			return valid
	
	return valid