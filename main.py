import re
import os
import glob
import json

def main():
    cwd = os.getcwd()
    os.chdir(cwd)
    # Make a List of all the Json files in the cwd
    json_files = glob.glob('*.json')

    uniqueVtpDomains = []
    def unique(list1): 
    # insert the list to the set 
        list_set = set(list1)
        # convert the set to the list 
        unique_list = (list(list_set)) 
        for x in unique_list: 
            uniqueVtpDomains.append(x)
    
    def orderByVtpDomain(json_files):
        pattern = re.compile(r'vtp_status_facts-([^,\s]+).json')
        matches = filter(pattern.search, json_files)
    
        interface_hostnames = []
        if matches:
            for match in matches:
                interface_hostnames.append(pattern.search(match).group(1))

        vtp_domains = []
        vtpDomainsAndSameVlans = {'domain':[]}
        counter = 0

        for item in interface_hostnames:
            with open('vtp_status_facts-{}.json'.format(interface_hostnames[counter])) as vtp_file:
                vtp_data = json.loads(vtp_file.read())
                vtp_domains.append(vtp_data['vtp_domain'])
                counter += 1
                
        unique(vtp_domains)

        i = 0
        for item in interface_hostnames:
            with open('vtp_status_facts-{}.json'.format(interface_hostnames[i])) as vtp_file:
                vtp_data = json.loads(vtp_file.read())
                for domain in uniqueVtpDomains:
                    if vtp_data['vtp_domain'] == domain:
                        for item in vtpDomainsAndSameVlans:
                            if vtp_data['vtp_domain'] in vtpDomainsAndSameVlans:
                                vtpDomainsAndSameVlans[item].append(vtp_data)
                                print(1)
        
        item_list_interface = {}
        sameVtpDomain = {}
    orderByVtpDomain(json_files)
    
if __name__== "__main__":
  main()
