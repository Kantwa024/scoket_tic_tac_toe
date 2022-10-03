import re
import socket    
import json
from time import time 
from termcolor import colored
import threading

class UnitClient:
    def __init__(self, port = None, ip_address = None) -> None:
        self.__socket = None
        self.__port = None
        self.__data_lnth = 16384
        self.__ip_address = None
        self.__data = {}
        self.__setPort(port)
        self.__setIpAddress(ip_address)
    
    def getStateOfData(self):
        return self.__data

    def setByteDataLength(self, data_lnth):
        if self.__checkByteDataLength(data_lnth):
            self.__data_lnth = data_lnth
            print (colored("Successfully changed data_lnth value", "green"))
            return True


    def sendDataToServer(self, data):
        try:
            data = json.dumps(data)
            self.__socket.sendall(bytes(data,encoding="utf-8"))
            print(colored("Data sent successfuly", "green"))
            return True
        except Exception as e:
            print(colored("Error sendDataToServer() function:\n" + str(e), "red"))
            return False
    
    
    def connectToServer(self):
        try:
            self.__createSocket()
        except Exception as e:
            print(colored("Error connectToServer() function:\n" + str(e), "red"))


    def __setIpAddress(self, ip_address):
        if self.__checkIdAddressType(ip_address):
            self.__ip_address = ip_address
            print (colored("Successfully changed ip_address value", "green"))
            return True

    def __checkIdAddressType(self, ip_address):
        try:
            if isinstance(ip_address, str):
                return True
            else:
                raise Exception("Error in checkIdAddressType() function:\n" + "ip_address type should be str")
        except Exception as e:
            raise Exception("Error in checkIdAddressType() function:\n" + str(e))


    def __setPort(self, port):
        if self.__checkPortType(port):
            if not self.__port:
                self.__port = port
                print (colored("Successfully changed port value", "green"))
                return True
            else:
                print (colored("Port value already exist", "red"))
                return False

    def __checkPortType(self, port):
        try:
            if isinstance(port, int):
                return True
            else:
                raise Exception("Error in checkPortType() function:\n" + "port type should be int")
        except Exception as e:
            raise Exception("Error in checkPortType() function:\n" + str(e))
    
    
    def __checkByteDataLength(self, data_lnth):
        try:
            if isinstance(data_lnth, int):
                return True
            else:
                raise Exception("Error in checkByteDataLength() function:\n" + "data_lnth type should be int")
        except Exception as e:
            raise Exception("Error in checkByteDataLength() function:\n" + str(e))


    def __createSocket(self):
        try:
            if not self.__socket:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print (colored("Socket successfully created", "green"))
                self.__connectToSocket()
                return True
            print (colored("Socket already exist", "red"))
            return False
        except Exception as e:
            raise Exception("Error in createSocket() function:\n" + str(e))
    
    def __connectToSocket(self):
        try:
            if self.__socket:
                self.__socket.connect((self.__ip_address, self.__port))
                print (colored("socket connected to port %s" %(self.__port), "green"))
                self.__getDataFromServer()
                return True
            else:
                raise Exception("Error inconnectToSocket() function:\n" + "socket value can not be none")
        except Exception as e:
            raise Exception("Error in connectToSocket() function:\n" + str(e))


    def __getDataFromServer(self):
        try:
            my_thread = threading.Thread(target = self.__getDataFromServerThread)
            my_thread .start()
        except Exception as e:
            raise Exception("Error in getDataFromServer() function:\n" + str(e))


    def __getDataFromServerThread(self):
        while True:
            try:
                data = json.loads(self.__socket.recv(self.__data_lnth).decode())
                if 'connected' not in data:
                    self.__data = data
                    print(self.__data)
            except Exception as e:
                print(colored("Error getDataFromServerThread() function:\n" + str(e), "red"))
                break


