import unit_server as unitServer
from termcolor import colored

class MainServer:
    def __init__(self) -> None:
        self.__unitServers = {}
        self.__total_server = 0
    
    def getUnitServers(self):
        return self.__unitServers

    def getTotalServersCount(self):
        return self.__total_server
    
    def getNewUnitServer(self, id, port, max_connections):
        key = (id, port)
        if key not in self.__unitServers:
            unit_server = unitServer.UnitServer(port, max_connections)
            unit_server.connectToClients()
            self.__unitServers[key] = unit_server
            print(colored("Your UnitServer id and port " + id + " "+ str(port), "green"))
            self.__total_server += 1
        else:
            print(colored("Please choose diffrent id and port number", "red"))
    
    def closeUnitServerByIdandPort(self, id, port):
        key = (id, port)
        if key in self.__unitServers:
            try:
                self.__unitServers[key].closeSocket()
                del self.__unitServers[key]
                self.__total_server -= 1

                print (colored("Closed successfuly", "green"))
            except Exception as e:
                raise Exception("Error in closeUnitServerByIdandPort() function:\n" + e)
        else:
            print(colored("id and port number does not exist", "red"))
    
    def getMyUnitServerByIdandPort(self, id, port):
        key = (id, port)
        if key in self.__unitServers:
            return self.__unitServers[key]
        else:
            print(colored("id and port number does not exist", "red"))
    
    def closeAllTheUnitServers(self):
        for key, unit_server in self.__unitServers.items():
            try:
                unit_server.closeSocket()
            except:
                pass

        self.__total_server = 0
        self.__unitServers = {}
        print(colored("Successfuly closed all the unit servers", "green"))
    
    def printAllServers(self):
        for key, val in self.__unitServers.items():
            print(colored(str(key) + ": "+ str(val), "green"))

            
