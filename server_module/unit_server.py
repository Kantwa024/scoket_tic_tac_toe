import socket
from sys import flags
import threading
import time
import json
from termcolor import colored
  
class UnitServer:
    def __init__(self, port = None, max_connections = None) -> None:
        self.__socket = None
        self.__max_allowable_connections = 10
        self.__connections_dict = {}
        self.__connect_cnt = 1
        self.__current_connections = 0
        self.__delete_timeout = 1
        self.__data = {}
        self.__data_lnth = 16384
        self.__port = None
        self.__max_connections = 10
        self.__setPort(port)
        self.setMaxConnections(max_connections)
    
    def connectToClients(self):
        if self.__connect_cnt == 1:
            self.__connect_cnt -= 1
            self.__connectToClients()
        else:
            print(colored('Can not create multiple server in a UnitServer','red'))

    def disconnectToClients(self):
        try:
            for address, connection in self.__connections_dict.items():
                try:
                    connection.close()
                except:
                    pass
            print(colored("Successfuly disconnected all clients.", "green"))
            self.__connections_dict = {}
            self.__current_connections = 0
        except Exception as e:
            raise Exception("Error in disconnectToClients() function:\n" + str(e))

    def getStatus(self):
        if self.__socket:
            print(colored("Running", "green"))
        else:
            print(colored("Closed", "red"))
        
    def getByteDataLength(self):
        return self.__data_lnth

    def getData(self):
        return self.__data

    def getCurrentConnections(self):
        return self.__current_connections

    def getPort(self):
        return self.__port
    

    def getMaxConnections(self):
        return self.__max_connections


    def getMaxAllowableConnections(self):
        return self.__max_allowable_connections
    
    
    def closeSocket(self):
        try:
            self.__socket.close()
            self.__socket = None
            return True
        except Exception as e:
            raise Exception("Error in closeSocket() function:\n" + str(e))

    def setMaxAllowableConnections(self, max_allowable_connections):
        if self.__checkMaxAllowableConnections(max_allowable_connections):
            self.__max_allowable_connections = max_allowable_connections
            print (colored("Successfully changed max_allowable_connections value", "green"))
            return True
    

    def setMaxConnections(self, max_connections):
        if self.__checkMaxConnectionsType(max_connections):
            self.__max_connections = max_connections
            print (colored("Successfully changed max_connections value", "green"))
            return True

    def setByteDataLength(self, data_lnth):
        if self.__checkByteDataLength(data_lnth):
            self.__data_lnth = data_lnth
            print (colored("Successfully changed data_lnth value", "green"))
            return True


    def __setPort(self, port):
        if self.__checkPortType(port):
            if not self.__port:
                self.__port = port
                print (colored("Successfully changed port value", "green"))
                return True
            else:
                print (colored("Port value already exist", "red"))
                return False

    def __checkByteDataLength(self, data_lnth):
        try:
            if isinstance(data_lnth, int):
                return True
            else:
                raise Exception("Error in checkByteDataLength() function:\n" + "data_lnth type should be int")
        except Exception as e:
            raise Exception("Error in checkByteDataLength() function:\n" + str(e))

    def __checkMaxAllowableConnections(self, max_allowable_connections):
        try:
            if isinstance(max_allowable_connections, int):
                return True
            else:
                raise Exception("Error in checkMaxAllowableConnections() function:\n" + "max_allowable_connections type should be int")
        except Exception as e:
            raise Exception("Error in checkMaxAllowableConnections() function:\n" + str(e))


    def __checkPortType(self, port):
        try:
            if isinstance(port, int):
                return True
            else:
                raise Exception("Error in checkPortType() function:\n" + "port type should be int")
        except Exception as e:
            raise Exception("Error in checkPortType() function:\n" + str(e))


    def __checkMaxConnectionsType(self, max_connections):
        try:
            if isinstance(max_connections, int):
                if max_connections <= self.__max_allowable_connections:
                    return True
                raise Exception("Error in checkMaxConnectionsType() function:\n" + "max_connections can not exceed max_allowable_connections: " + str(self.__max_allowable_connections)) 
            else:
                raise Exception("Error in checkMaxConnectionsType() function:\n" + "max_connections type should be int")
        except Exception as e:
            raise Exception("Error in checkMaxConnectionsType() function:\n" + str(e))


    def __createSocket(self):
        try:
            if not self.__socket:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print (colored("Socket successfully created", "green"))
                return True
            print (colored("Socket already exist", "red"))
            return False
        except Exception as e:
            raise Exception("Error in createSocket() function:\n" + str(e))
    

    def __bindSocket(self):
        try:
            if self.__socket:
                self.__socket.bind(('', self.__port))        
                self.__socket.listen(10**6)   

                print (colored("socket binded to %s" %(self.__port), "green"))
                print (colored("socket is listening", "green"))
                return True
            else:
                raise Exception("Error in bindSocket() function:\n" + "socket value can not be none")
        except Exception as e:
            raise Exception("Error in bindSocket() function:\n" + str(e))
    

    def __connectToClients(self):
        try:
            if self.__createSocket():
                if self.__bindSocket():
                    my_thread = threading.Thread(target = self.__connectToClientsThread)
                    my_thread.setDaemon(True)
                    my_thread .start()
        except Exception as e:
            raise Exception("Error in connectToClients() function:\n" + str(e))

    def __sendDataToClient(self, connection, data):
        try:
            data = json.dumps(data)
            connection.sendall(bytes(data,encoding="utf-8"))
            return True
        except Exception as e:
            return False

    def __removeDisconnectedClients(self):
        running_dict, connection_cnt = {}, 0
        for address, connection in self.__connections_dict.items():
            if self.__sendDataToClient(connection, {'connected': address}):
                running_dict[address] = connection
                connection_cnt += 1

        self.__connections_dict = running_dict
        self.__current_connections = connection_cnt
        self.__getDataFromEashConnection()


    def __eachSecond(self):
        try:
            my_thread = threading.Thread(target = self.__eachSecondThread)
            my_thread.setDaemon(True)
            my_thread .start()
        except Exception as e:
            raise Exception("Error in eachSecond() function:\n" + str(e))

    def __eachSecondThread(self):
        while True:
            try:
                self.__removeDisconnectedClients()
            except:
                pass
            time.sleep(self.__delete_timeout)
    
    def __changeDataState(self, new_data):
        try:
            for key, val in new_data.items():
                self.__data[key] = val

            self.__sendDataToEashConnection()
        except Exception as e:
            pass
    

    def __getDataFromConnection(self, address, connection):
        try:
            my_thread = threading.Thread(target = self.__getDataFromConnectionThread, args= (connection, ))
            my_thread.setDaemon(True)
            my_thread .start()
        except Exception as e:
            raise Exception("Error in connectToClients() function:\n" + str(e))


    def __getDataFromConnectionThread(self, connection):
        while True:
            try:
                conn_data = json.loads(connection.recv(self.__data_lnth).decode())
                self.__changeDataState(conn_data)
            except Exception as e:
                break
    
    def __sendDataToEashConnection(self):
        try:
            for address, connection in self.__connections_dict.items():
                self.__sendDataToClient(connection, self.__data)
        except Exception as e:
            pass

    def __connectToClientsThread(self):
        self.__eachSecond()
        while True:
            try:
                connection, address = self.__socket.accept()
                # print ('Got connection from', address)

                if self.__current_connections < self.__max_connections:    
                    self.__sendDataToClient(connection, self.__data)

                    self.__current_connections += 1
                    self.__connections_dict[address] = connection
                    self.__getDataFromConnection(address, connection)
                else:
                    self.__sendDataToClient(connection, {'connected': False, 'message' : 'Server is very busy'})
                    connection.close()
                    # print("Can not connect " + str(address) + "\nMax connection limit reached")
            except Exception as e:
                break

    
