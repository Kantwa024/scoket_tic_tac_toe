from time import sleep
from termcolor import colored
import main_server as mainServer
import uuid
import random

class RunServer:
    def __init__(self) -> None:
        self.__mainServer = mainServer.MainServer()
        self.__cache_data = None
        self.__unitServer = None

    def runConsole(self):
        while True:
            try:
                dicts = {'Add unitServer': '1', 'Remove unitServer': '2', 'Connect to Unit Server': '3', 
                'Get Byte Data Length': '4', 'Get Data': '5', 'Get Current Connections': '6', 
                'Get Port': '7', 'Get Max Connections': '8', 'Get Max Allowable Connections': '9', 
                'Close Socket': '10', 'Set Max Allowable Connections': '11', 'Set Max Connections': '12', 
                'Set Byte Data Length': '13', 'Clean Cache Data': '14', 'Close All Unit Servers': '15', 
                'Disconnect to Clients': '16', 'Totol Servers Count': '17', 'Get Total Servers List': 
                '18', 'Get Unit Server Status': '19'}

                lst_oprations = list(dicts.keys())
                lst_oprations.sort()

                dicts['Stop'] = '20'
                lst_oprations.append('Stop')
                
                print()
                for i in range(len(lst_oprations)):
                    print(str(i+1) + ". " + lst_oprations[i])
                print()

                n = int(input("Please enter a number in between 1 and 20:\n"))
                
                n = int(dicts[lst_oprations[n - 1]])
                
                if n == 20:
                    print(colored("Thank you for using", "green"))
                    break
                
                if n == 1 or n == 3:
                    self.__cache_data = None

                if not self.__cache_data:
                    id = input("Please enter unitServer id (for option 1 it is optional):\n")
                    port = input("Please enter unitServer port number (for option 1 it is optional):\n")
                    max_connections = input("Please enter unitServer max_connections number (only for option 1):\n")

                    if len(id.strip()) == 0:
                        id= uuid.uuid1().hex
                    else:
                        pass

                    if len(port.strip()) == 0:
                        port = random.randint(0, 65535)
                    else:
                        port = int(port)

                    if len(max_connections.strip()) == 0:
                        max_connections = 10
                    else:
                        max_connections = int(max_connections)
                    
                    self.__cache_data = {
                        'id': id,
                        'port': port,
                        'max_connections': max_connections
                    }

                self.__allIfandElseConditions(n)

            except Exception as e:
                print(colored("Error in runConsoleThread() function:\n" + str(e),'red'))
    
    def __checkUnitServerState(self):
        if self.__unitServer:
            return True

        print(colored("Please create or connect with unit server",'red'))
        return False

    def __checkIntType(self, data):
        try:
            if isinstance(data, int):
                return True
            else:
                raise Exception("Error in checkIntType() function:\n" + "data_lnth type should be int")
        except Exception as e:
            raise Exception("Error in checkIntType() function:\n" + str(e))

    def __allIfandElseConditions(self, n):
        try:
            id, port, max_connections = self.__cache_data['id'], self.__cache_data['port'], self.__cache_data['max_connections']
            key = (id, port)

            if n == 1:
                self.__mainServer.getNewUnitServer(id, port, max_connections)
                self.__unitServer = self.__mainServer.getUnitServers().get(key)
                print(colored(self.__unitServer, "green"))

            elif n == 2:
                self.__mainServer.closeUnitServerByIdandPort(id, port)

            elif n == 3:
                unit_server = self.__mainServer.getUnitServers().get(key)
                if unit_server != None:
                    self.__unitServer = unit_server
                    print(colored("Successfully Connected", "green"))
                else:
                    print(colored("Please enter a valid id and port number", "red"))

            elif n == 4:
                if self.__checkUnitServerState():
                    print(colored(self.__unitServer.getByteDataLength(), "green"))
            
            elif n == 5:
                if self.__checkUnitServerState():
                    print(colored(self.__unitServer.getData(), "green"))
            
            elif n == 6:
                if self.__checkUnitServerState():
                    print(colored(self.__unitServer.getCurrentConnections(), "green"))

            elif n == 7:
                if self.__checkUnitServerState():
                    print(colored(self.__unitServer.getPort(), "green"))

            elif n == 8:
                if self.__checkUnitServerState():
                    print(colored(self.__unitServer.getMaxConnections(), "green"))

            elif n == 9:
                if self.__checkUnitServerState():
                    print(colored(self.__unitServer.getMaxAllowableConnections(), "green"))

            elif n == 10:
                if self.__checkUnitServerState():
                    if self.__unitServer.closeSocket():
                        print(colored("Socket closed successfuly", "green"))

            elif n == 11:
                if self.__checkUnitServerState():
                    cnt = int(input("Please enter max allowabe connections:\n"))
                    if self.__checkIntType(cnt):
                        self.__unitServer.setMaxAllowableConnections(cnt)


            elif n == 12:
                if self.__checkUnitServerState():
                    cnt = int(input("Please enter max connections:\n"))
                    if self.__checkIntType(cnt):
                        self.__unitServer.setMaxConnections(cnt)


            elif n == 13:
                if self.__checkUnitServerState():
                    cnt = int(input("Please enter byte data length:\n"))
                    if self.__checkIntType(cnt):
                        self.__unitServer.setByteDataLength(cnt)

            elif n == 14:
                self.__unitServer = None
                self.__cache_data = {}
                print(colored("Cache cleared successfully.", "green"))

            elif n == 15:
                self.__mainServer.closeAllTheUnitServers()

            elif n == 16:
                if self.__checkUnitServerState():
                    self.__unitServer.disconnectToClients()

            elif n == 17:
                print(colored("Total Servers: " + str(self.__mainServer.getTotalServersCount()), "green"))
            
            elif n == 18:
                self.__mainServer.printAllServers()
            
            elif n == 19:
                if self.__checkUnitServerState():
                    self.__unitServer.getStatus()               
            
        except Exception as e:
            raise Exception("Error in allIfandElseConditions() function:\n" + str(e))


console = RunServer()
console.runConsole()