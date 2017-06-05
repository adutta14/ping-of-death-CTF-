from ictf import iCTF
import os
import json, ast

def encode_dict(d, codec='utf8'):
    ks = d.keys()
    for k in ks:
        val = d.pop(k)
        if isinstance(val, unicode):
            val = val.encode(codec)
        elif isinstance(val, dict):
            val = encode_dict(val, codec)
        if isinstance(k, unicode):
            k = k.encode(codec)
        d[k] = val
    return d

i = iCTF('http://52.34.158.221/')
t = i.login('team1@example.com','password')
key_info = t.get_ssh_keys()

with open('ctf_key', 'wb') as f:
	f.write(key_info['ctf_key'])

with open('root_key', 'wb') as f:
	f.write(key_info['root_key'])

print key_info['ip']
print key_info['port']

print t.get_service_list()

ip = key_info['ip']
port_no = str(key_info['port'])
path_to_key = 'ctf_key'

chmod_command = "chmod 600 ctf_key"
os.system(chmod_command)
chmod_command = "chmod 600 root_key"
os.system(chmod_command)

ssh_command = "ssh -i " + path_to_key + " -p"+ port_no + " ctf@" + ip

os.system(ssh_command)
print "HELLO"
r= t.get_service_list()
#print r
for ss in r:
    print "sho"
    print ss['service_id']
    print t.get_targets(ss['service_id'])


os.system("exit")