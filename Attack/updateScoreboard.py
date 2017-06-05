from ictf import iCTF
import os
import time
# import paramiko
import json, ast
import thread
import json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
print(config)


# Login to iCTF server and get ssh keys of our server
ictf = iCTF(config["ctf_ip"])
t = ictf.login(config["team_id"],config["team_pass"])
key_info = t.get_ssh_keys()
print json.dumps(key_info, indent=4, sort_keys=True)


t.submit_flag(["FLGbTEYSdNA4qhnr", "FLG2W0f5G8bbt3sK"])

print "Flag submitted..."


