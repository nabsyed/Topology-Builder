import access
import getpass
import layers
import os

def seed_device():
	
	seed_device = raw_input("\nEnter seed device hostname: ")
	device_type = seed_device[seed_device.find("-") + 1 : seed_device.find("-") + 3]
	layers_list = layers.layers_list()
	
	if (len(seed_device) < 9) or (device_type not in layers_list):
		while (len(seed_device) < 9) or (device_type not in layers_list):
			seed_device = raw_input("Enter a valid seed device hostname: ")
			device_type = seed_device[seed_device.find("-") + 1 : seed_device.find("-") + 3]
	return seed_device

def upper_limit():
	layers_list = layers.layers_list()
	
	print "\nEnter upper limit of device hierarchy. Valid inputs include:", ','.join(layers_list)
	upper_limit = raw_input("Upper limit: ")
	if (len(upper_limit) is 0) or (upper_limit not in layers_list):
		while (len(upper_limit) is 0) or (upper_limit not in layers_list):
			upper_limit = raw_input("Enter a valid upper limit: ")
	return upper_limit

def lower_limit(upper_lim):
	layers_list = layers.layers_list()
	
	print "\nEnter lower limit of device hierarchy. Valid inputs include:", ','.join(layers_list[int(layers.layers_dict(upper_lim)):len(layers_list)])
	lower_limit = raw_input("Lower limit: ")
	
	if ((len(lower_limit) is 0) or (lower_limit not in layers_list) or (int(layers.layers_dict(lower_limit)) <= int(layers.layers_dict(upper_lim)))):
		while (len(lower_limit) is 0) or (lower_limit not in layers_list) or (int(layers.layers_dict(lower_limit)) <= int(layers.layers_dict(upper_lim))):
			lower_limit = raw_input("Enter a valid lower limit: ")
	return lower_limit

def location_code():	
	print "\nEnter location code, e.g. phx1, slc, lvs3"
	location_code = raw_input("Location code: ")
	if (len(location_code) < 3):
		while (len(location_code) < 3):
			location_code = raw_input("Enter a valid location code: ")
	return location_code	
	
def username():
	username = raw_input("\nUsername: ")
	if len(username) is 0:
		while len(username) is 0:
			username = raw_input("Enter a valid username: ")
	return username

def password():
	password = getpass.getpass("Password: ")
	return password

def auth_check(device):
	usr = username()
	pwd = password()
	
	auth_tries = 0
	max_auth_tries = False
	
	check = access.ssh_ndp(device,'',usr,pwd)

	if 'auth_fail' in check:
		while ('auth_fail' in check) and (auth_tries < 3):
			auth_tries+=1
			
			if auth_tries is 3:
				max_auth_tries = True
				break
				
			print "\nAttempt #:%d" %(auth_tries+1)
			usr = username()
			pwd = password()
			check = access.ssh_ndp(device,'',usr,pwd)
			
	return usr,pwd,max_auth_tries

def graph_type():
	print "\nEnter graph type desired. Valid inputs include:\n\t\t\t\t 'o'  = orthographic lines\n\t\t\t\t 'no' = non-overlapping lines\n\t\t\t\t 's'  = straight lines"

	graph_type_desired = raw_input("Enter graph type: ")
	if graph_type_desired not in ['o', 'no', 's']:
		while graph_type_desired not in ['o', 'no', 's']:
			graph_type_desired = raw_input("Enter valid graph type: ")
	
	if graph_type_desired == 'o':
		graph_type_desired = 'ortho'
	elif graph_type_desired == 'no':
		graph_type_desired = 'spline'
	elif graph_type_desired == 's':
		graph_type_desired = 'line'
	
	return graph_type_desired
	
def interface_labels():
	interface_labels_desired = raw_input("\nInterface labels? [y/n]: ")
	if interface_labels_desired not in ['y', 'n']:
		while interface_labels_desired not in ['y', 'n']:
			interface_labels_desired = raw_input("Enter valid response: ")
			
	return interface_labels_desired

def file_append():
	print "\nWhich topology file do you want to modify?\n"
	os.system("ls -l img | grep topology")
	print "\nEnter filename suffix (after 'topology-' up to '.')"
	file_append_desired = raw_input("\nFilename suffix: ")
	
	return file_append_desired
		
def banner():
	os.system ("clear")	
	longstring = """\
	
	
	
	
	
	
 /$$$$$$$$                            /$$                                     /$$$$$$$            /$$ /$$       /$$                    
|__  $$__/                           | $$                                    | $$__  $$          |__/| $$      | $$                    
   | $$  /$$$$$$   /$$$$$$   /$$$$$$ | $$  /$$$$$$   /$$$$$$  /$$   /$$      | $$  \ $$ /$$   /$$ /$$| $$  /$$$$$$$  /$$$$$$   /$$$$$$ 
   | $$ /$$__  $$ /$$__  $$ /$$__  $$| $$ /$$__  $$ /$$__  $$| $$  | $$      | $$$$$$$ | $$  | $$| $$| $$ /$$__  $$ /$$__  $$ /$$__  $$
   | $$| $$  \ $$| $$  \ $$| $$  \ $$| $$| $$  \ $$| $$  \ $$| $$  | $$      | $$__  $$| $$  | $$| $$| $$| $$  | $$| $$$$$$$$| $$  \__/
   | $$| $$  | $$| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$| $$  | $$      | $$  \ $$| $$  | $$| $$| $$| $$  | $$| $$_____/| $$      
   | $$|  $$$$$$/| $$$$$$$/|  $$$$$$/| $$|  $$$$$$/|  $$$$$$$|  $$$$$$$      | $$$$$$$/|  $$$$$$/| $$| $$|  $$$$$$$|  $$$$$$$| $$      
   |__/ \______/ | $$____/  \______/ |__/ \______/  \____  $$ \____  $$      |_______/  \______/ |__/|__/ \_______/ \_______/|__/      
                 | $$                               /$$  \ $$ /$$  | $$                                                                
                 | $$                              |  $$$$$$/|  $$$$$$/                                                                
                 |__/                               \______/  \______/                                                                 
                                                              /$$         /$$                                                          
                                                            /$$$$       /$$$$                                                          
                                                 /$$    /$$|_  $$      |_  $$                                                          
                                                |  $$  /$$/  | $$        | $$                                                          
                                                 \  $$/$$/   | $$        | $$                                                          
                                                  \  $$$/    | $$        | $$                                                          
                                                   \  $/    /$$$$$$ /$$ /$$$$$$                                                        
                                                    \_/    |______/|__/|______/                                                        
                                                                                                                                       
                                                                                                                                       
         
										
	"""
	print longstring