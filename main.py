import re
import os
import glob
import json

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
    #List vlans with same vtp domains
    domain_and_vlans = {}

    i = 0
    for item in interface_hostnames:
        with open('vtp_status_facts-{}.json'.format(interface_hostnames[i])) as vtp_file, open('interfaces_status_facts-{}.json'.format(interface_hostnames[i])) as vlan_file:
            vtp_data = json.loads(vtp_file.read())
            vlan_data = json.loads(vlan_file.read())
            domain = vtp_data['vtp_domain']
            
            for item,key in vlan_data.items():
                vlan = key['data']['vlan']
                #check if domain in dictonary, if not update it with dictonary
                if domain in domain_and_vlans and vlan in domain_and_vlans[domain]:
                    vlan_counter = domain_and_vlans[domain].get(vlan)
                    vlan_counter += 1
                    domain_and_vlans[domain].update({vlan: vlan_counter})
                    print(domain_and_vlans)
                else:
                    domain_and_vlans.update({domain: {vlan: 1}})
            i += 1

def main():
    #Outputs list of unique vtp domains
    cwd = os.getcwd()
    os.chdir('interfaces/')
    # Make a List of all the Json files in the cwd
    json_files = glob.glob('*.json')
    order_by_vtp_domain(json_files)

if __name__ == '__main__':
    main()