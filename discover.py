import access
import catos
import ios_cdp
import ios_lldp
import iosxr_cdp
import iosxr_lldp
import nxos_cdp
import nxos_lldp
import eos
import junos
import time


def get_ndp_output (current_node,usr,pwd,file_append,output_nodes,output_links):

	accessed_file = open ('data/accessed-%s.txt' %file_append, 'a')

	access_start_time = time.time()
	unique = []			# In case 'access' / parser return an error
	error_code = "normal"

	nos = access.ssh_ver (current_node,'show version',usr,pwd)
	if 'SSH_Error' in nos:
		error_code = nos					# 'nos' in this case is the SSH exception returned from 'access.py'
		nos = 'Unknown_due_to_SSH_error'

	
	if (nos == 'ios'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',usr,pwd)
		if 'SSH_Error' in cdp_out:
			error_code = cdp_out
		else:
			unique = ios_cdp.parser(cdp_out, current_node,  file_append,output_links)

			lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',usr,pwd)
			if "enabled" not in lldp_out:
				lldp = ios_lldp.parser(lldp_out, current_node, unique,  file_append,output_links)
				unique.extend(lldp)
	elif (nos == 'nxos'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',usr,pwd)
		if 'SSH_Error' in cdp_out:
			error_code = cdp_out
		else:
			unique = nxos_cdp.parser(cdp_out, current_node,  file_append,output_links)

			lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',usr,pwd)
			lldp = nxos_lldp.parser(lldp_out, current_node, unique,  file_append,output_links)
			unique.extend(lldp)
	elif (nos == 'iosxr'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',usr,pwd)
		if 'SSH_Error' in cdp_out:
			error_code = cdp_out
		else:
			unique = iosxr_cdp.parser(cdp_out, current_node,  file_append,output_links)

			lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',usr,pwd)
			lldp = iosxr_lldp.parser(lldp_out, current_node, unique,  file_append,output_links)
			unique.extend(lldp)
	elif (nos == 'catos'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',usr,pwd)
		if 'SSH_Error' in cdp_out:
			error_code = cdp_out
		else:
			unique = catos.parser(cdp_out, current_node,  file_append,output_links)
	elif (nos == 'eos'):
		lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',usr,pwd)
		if 'SSH_Error' in lldp_out:
			error_code = lldp_out
		else:
			unique = eos.parser(lldp_out, current_node,  file_append,output_links)
	elif (nos == 'junos'):
		lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',usr,pwd)
		if 'SSH_Error' in lldp_out:
			error_code = lldp_out
		else:
			unique = junos.parser(lldp_out, current_node,  file_append,output_links)


	access_time = time.time() - access_start_time
	accessed_file.write (current_node + "\t" + nos + "\t" + str("%0.2f" %access_time) + "\t" + error_code +"\n")

	if error_code != 'normal':
		unique = []

#	print "Current Node:", current_node,":", unique

	output_nodes.put(unique)
