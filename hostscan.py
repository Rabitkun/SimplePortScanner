import socket as SCK
import threading as TH
import os
import platform

def getBroadcastIP(IP):
    result = IP.split('.')
    return f"{'.'.join(result[:3])}"

def getLocalIPs():
    host_name = SCK.gethostname()
    ip_addresses = SCK.gethostbyname_ex(host_name)
    return ip_addresses[2]

def getPingCommand():
    operation_system = platform.system()
    result = "ping"
    if (operation_system == "Windows"):
        result = f"{result} -n 1 "
    else:
        result = f"{result} -c 1 "
    return result

def checkHostByIP(ip, output = []):
    command = f"{getPingCommand()}{ip}"
    response = os.popen(command)
    data = response.readlines()
    for line in data:
        if 'TTL' in line:
            print(ip, "--> Ping Ok")
            output.append(ip)
            break
    return output

def getLocalHostsIP(hostIP = ""):
    hosts = []
    threads = [] 
    localIP = hostIP
    if hostIP == "": localIP = getLocalIPs()[0]
    broadcastIP = getBroadcastIP(localIP)
    for i in range(255):
        destinationIP = f"{broadcastIP}.{i}"
        thread = TH.Thread(target = checkHostByIP, kwargs={'ip': destinationIP, 'output' : hosts})
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return hosts

if __name__ == "__main__":
    ips = getLocalIPs()
    print(getLocalHostsIP())
