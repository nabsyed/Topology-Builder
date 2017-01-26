# Topology Builder v1.1

This is a fully functional topology builder. The software simply automates what network administrators have done manually for many years: use CDP and LLDP on the device CLI to find the device's connected neighbors and iteratively develop a diagram of the network. 

Mode of Operation:
- The device starts of with accessing a "seed" device. This is where the software starts its 'crawl' process
- The software discovers the seed device's unique neighbors
- It then accesses each neighbors' neighbors. With each iteration, it records the unique links from the device to its neighbors
- It continues this process until all discovered neighbors have been accessed and no new neighbors are discovered
- It then uses Graphviz to plot or graph the unique links
- It also lays out the nodes discovered in network hierarchies, like core, distribution, access etc.

Requirements for software to work:
- CDP or LLDP enabled on all network devices
- Device reachability via SSHv2
- Consistent naming scheme for device hostnames
- Hierarchical network design

Current parsers supported:
- Cisco CatOS
- Cisco IOS (and IOS-XE)
- Cisco NX-OS
- Cisco IOS-XR
- Arista EOS
- Juniper Junos OS

Limitations:
- Does not see through firewalls
- No SNMP support

Improvements under consideration:
- Graphical front-end
- Ability to define your device naming convention at initialization
- D3 for graphing, instead of Graphviz

How to adapt it to your environment:
- Install python
- Install pydot
- Install graphviz
- Install paramiko
- Install natsort
- Modify "layers.py" to define your network hierarchies
- Modify "device-type" and other files to suit your device naming convention (more details on this to follow...)
