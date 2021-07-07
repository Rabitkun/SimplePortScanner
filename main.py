import portscan as PS
import hostscan as HS

def getInputAndPrintCommandList(commands_list):
    print("-"*50)
    for i in range(len(commands_list)):
        print(f"[{i}] - {commands_list[i]}")
    return input("Input valid number of command from list: ")

def inputPorts():
    ports = input("Enter ports to scan: ")
    if "-" in ports: 
        ports = list(map(int, ports.split('-')))
        ports = range(ports[0], ports[1])
    else:
        ports = ports.split(' ')
        ports = list(map(int, ports))

    return ports

def portScanMenuLoop(IP):
    while True:
        command = getInputAndPrintCommandList(("Scan local Network to search hosts","Scan ports TCP","Scan ports UDP", "Back"))
        scanner = PS.PortScanner(IP)
        if command == "0":
            hosts = HS.getLocalHostsIP(IP)
        elif command == "1":
            ports = inputPorts()
            scanner.scanPorts(ports, PS.PT_TCP)
        elif command == "2":
            ports = inputPorts()
            scanner.scanPorts(ports, PS.PT_UDP)
        elif command == "3":
            break
        else:
            continue

def chooseLocalIPLoop():
    ip = ""

    return ip        

def mainLoop():
    while True:
        command = getInputAndPrintCommandList(("Enter host IP to Scan", "Show local IPs list", "Auto getting local IP", "Exit"))
        if command == "0":
            ip = input("Input host IP: ")
            portScanMenuLoop(ip)
        elif command == "1":
            ips = HS.getLocalIPs()
            print("Local IPs:")
            for ip in ips: print(f"| {ip}")
        elif command == "2":
            ip = HS.getLocalIPs()[0]
            print(f"| Host IP: {ip}")
            portScanMenuLoop(ip)
        elif command == "3":
            break
        else:
            continue



if __name__ == "__main__":
    mainLoop()