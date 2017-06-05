from ictf import iCTF
import os
import time
import json, ast
import thread
import re
fails={}
IP = '172.31.129.'
count=0

# Config File read
import json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
print(config)


# Login to iCTF server and get ssh keys of our server
ictf = iCTF(config["ctf_ip"])
t = ictf.login(config["team_id"],config["team_pass"])
key_info = t.get_ssh_keys()
print json.dumps(key_info, indent=4, sort_keys=True)

with open('Run_Status', 'wb') as f:
    f.write("\n")

with open('ctf_key', 'wb') as f:
    f.write(key_info['ctf_key'])

with open('root_key', 'wb') as f:
    f.write(key_info['root_key'])

chmod_command = "chmod 600 ctf_key"
os.system(chmod_command)
chmod_command = "chmod 600 root_key"
os.system(chmod_command)
