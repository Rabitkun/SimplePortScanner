import socket as SCK
import threading as TH

PT_TCP = 0 #for TCP Protocol scan
PT_UDP = 1 #for UDP Protocol scan

class PortScanner:
    def __init__(self, IP):
        self.IP = IP
        self.scanResult = {}

    def setIP(self, IP):
        self.IP = IP

    def scanPortTCP(self, port):
        connection = SCK.socket(SCK.AF_INET, SCK.SOCK_STREAM)
        connection.settimeout(1)
        isPortOpened = False
        try:
            bridge = connection.connect((self.IP, port))
            print(f'{port} Connected')
            isPortOpened = True
            bridge.close()
        except:
            if isPortOpened == False : print(f'{port} Unavaible')
        finally:
            self.scanResult[port] = isPortOpened

    def icmpCheck(self, connection, port): 
        try:
            if port == "80":
                connection.send("GET HTTP/1.1  \r\n")
            else:
                connection.send(" \r\n ")
                result = connection.recv(4096)	
                print(f"Service: {str(result)}\n")
        except:
            print("Service Unavailable!\n")

    def scanPortUDP(self, port):
        connection = SCK.socket(SCK.AF_INET, SCK.SOCK_DGRAM)
        isPortOpened = True
        try:
            bridge = connection.connect((self.IP,port))
            print(f'{port} Connected')
            self.icmpCheck(connection, port)
            isPortOpened = True
        except:
            isPortOpened = False
            print(f'{port} Unavailable')
        finally:
            self.scanResult[port] = isPortOpened

    def scanPorts(self, ports, protocol):
        self.scanResult = {}
        threads = []
        for port in ports:
            thread = TH.Thread(target = self.scanPortTCP if protocol == PT_TCP else self.scanPortUDP, kwargs={'port': port})
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            
        return self.scanResult

if __name__ == "__main__":
    scanner = PortScanner('109.195.211.23')
    #scanner.IP = "2ip.ru"
    print('TCP')
    ports = (86, 80, 3389, 443, 8888, 8080, 8081, 8082)
    ports = (22, 80, 443, 843, 8001, 23, 53, 8291, 3389)
    print(scanner.scanPorts(ports,PT_TCP))
    print('\nUDP')
    print(scanner.scanPorts((86, 80, 3389, 443, 8888, 8080, 8081, 8086),PT_UDP))
