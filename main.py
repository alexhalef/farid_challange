import re
import os
import glob
import json

def unique(list1):
    # insert the list to the set 
    list_set = set(list1)
    # convert the set to the list 
    unique_list = (list(list_set)) 
    for x in unique_list: 
        unique_vtp_domains.append(x)

#Not complete, order vlan in same vtp domain
def order_by_vtp_domain(json_files):
    pattern = re.compile(r'vtp_status_facts-([^,\s]+).json')
    matches = filter(pattern.search, json_files)
    #List of interface hostname
    interface_hostnames = []
    if matches:
        for match in matches:
            interface_hostnames.append(pattern.search(match).group(1))

    vtp_domains = []
    counter = 0
    #Loop interfaces vtp domains and list them
    for item in interface_hostnames:
        with open('vtp_status_facts-{}.json'.format(interface_hostnames[counter])) as vtp_file:
            vtp_data = json.loads(vtp_file.read())
            vtp_domains.append(vtp_data['vtp_domain'])
            counter += 1
    #List only unique vtp domains      
    unique(vtp_domains)
    #List vlans with same vtp domains
    domain_and_vlans = {}

    i = 0
    for item in interface_hostnames:
        with open('vtp_status_facts-{}.json'.format(interface_hostnames[i])) as vtp_file, open('interfaces_status_facts-{}.json'.format(interface_hostnames[i])) as vlan_file:
            vtp_data = json.loads(vtp_file.read())
            vlan_data = json.loads(vlan_file.read())
            domain = vtp_data['vtp_domain']

            if domain in domain_and_vlans:
                domain_and_vlans[domain].update({'vlan_name': 2})
            else: 
                domain_and_vlans.update({domain: {}})
            i += 1

    print(domain_and_vlans)
unique_vtp_domains = []
def main():
    #Outputs list of unique vtp domains
    cwd = os.getcwd()
    os.chdir('interfaces/')
    # Make a List of all the Json files in the cwd
    json_files = glob.glob('*.json')
    order_by_vtp_domain(json_files)

if __name__ == '__main__':
    main()