import paramiko, socket

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
paramiko.util.log_to_file("ssh_logs.log")

with open ('data/nos.txt', 'r') as nos_file:
	lines = nos_file.readlines()

nos_dict = {}	
	
for i in range (0, len(lines)):
	delimited = lines[i].split()
	nos_dict.update({delimited[0]:delimited[1]})

def ssh_ver (device,cmd,user,pw):

#	print "Accessing", device

	if nos_dict.get(device) != None:
		return nos_dict.get(device)
	else:
		pass						
	
	while True:
		try:
			ssh.connect(device, username=user, password=pw, timeout=20)
			stdin, stdout, stderr = ssh.exec_command(cmd)
			version = stdout.read().splitlines()
			
			for i in range (0, len(version)):
				if 'ios xr' in version[i].lower():
					nos = 'iosxr'
					break
				elif 'cisco ios' in version[i].lower():
					nos = 'ios'
					break
				elif 'nx-os' in version[i].lower():
					nos = 'nxos'
					break
				elif 'cat6000' in version[i].lower():
					nos = 'catos'
					break
				elif 'arista' in version[i].lower():
					nos = 'eos'
					break
				elif 'junos' in version[i].lower():
					nos = 'junos'
					break
				elif i == len(version):
					nos = 'Unknown NOS'
					break
			print nos
			return nos

		except socket.gaierror, e:
			print "\nError: Address resolution failed,", device
			return ("SSH_Error: addr_fail")
		except paramiko.AuthenticationException, e:
			print "\nError: Authentication failed,", device
			ssh.close()
			return ("SSH_Error: auth_fail")
		except socket.timeout, e:
			print "\nError: SSH timeout,", device
			ssh.close()
			return ("SSH_Error: ssh_timeout")
		except socket.error, e:
			print "\nError: Invalid hostname/IP address,", device
			ssh.close()
			return ("SSH_Error: invalid_address")
		except paramiko.SSHException, e:
			print "\nError: SSH Exception,", device
			ssh.close()
			return ("SSH_Error: ssh_exception")
		except:
			print "\nError:,", device
			ssh.close()
			return ("SSH_Error: SSH Error")
			
			
def ssh_ndp (device,cmd,user,pw):
	timeout_value = 5

	for i in range (3):
#		print "Try:", i+1
		try:
			ssh.connect(device, username=user, password=pw, timeout=timeout_value)
			stdin, stdout, stderr = ssh.exec_command(cmd)
			return stdout.read()			
		except socket.gaierror, e:
			print "\nError: Address resolution failed,", device
			return ("SSH_Error: addr_fail")
		except paramiko.AuthenticationException, e:
			print "\nError: Authentication failed,", device
			ssh.close()
			return ("SSH_Error: auth_fail")
		except socket.timeout, e:
			print "\nError: SSH timeout,", device
			ssh.close()
			timeout_value = timeout_value + 5
			if i > 1:
				return ("SSH_Error: ssh_timeout")
		except socket.error, e:
			print "\nError: Invalid hostname/IP address,", device
			ssh.close()
			return ("SSH_Error: invalid_address")
		except paramiko.SSHException, e:
			print "\nError: SSH Exception,", device
			ssh.close()
			return ("SSH_Error: ssh_exception")
		except:
			print "\nError:,", device
			ssh.close()
			return ("SSH_Error: SSH Error")
