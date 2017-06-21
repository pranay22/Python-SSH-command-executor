#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
SSH Command executor wrapper
Dependencies:
- OpenSSH
- libssl-dev
- PIP: Cryptography, Paramiko

Usages: 
connection = SSHCommandExecutor("<SERVER_ADDRESS>", "<SERVER_USERNAME>", "<SERVER_PASSWORD>")
connection.sendCommand("<COMMAND>")

@author: Pranay - 21/06/2017
'''

import logging
from paramiko import client

class SSHCommandExecutor(object):
    """ Base class for COmmand executor created from paramiko Python SSH lib
    """
    client = None
    
    def __init__(self, address, username, password):
        print ("Connecting to server through SSH")
        self.client = client.SSHClient()
        # following line is required if you want the script to be able to access a server that's not yet in the known_hosts file
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        # make the connection
        self.client.connect(address, username=username, password=password, look_for_keys=False)
	
    def sendCommand(self, command):
        """  This function will be used to send commands to the remote machine, after a connection in made
	"""
        # checking if connection is made previously
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # print stdout data when available
                if stdout.channel.recv_ready():
                    # retrieve the first 1024 bytes
                    alldata = stdout.channel.recv(1024)
                    while stdout.channel.recv_ready():
                        # retrieve the next 1024 bytes
                        alldata += stdout.channel.recv(1024)
                    # UTF8 encoding needed
                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")


if __name__=="__main__":
    log = logging.getLogger("CommandExecutorTest")
    log.setLevel(logging.INFO)
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #Specific formatter, can be changed if needed
    console.setFormatter(formatter)
    log.addHandler(console)
    connection = SSHCommandExecutor("<SERVER_ADDRESS>", "<SERVER_USERNAME>", "<SERVER_PASSWORD>")	#All should be in string
    connection.sendCommand("<COMMAND>")
    connection.sendCommand("cd folder")
    connection.sendCommand("mkdir test-folder")
    connection.sendCommand("cd folder && mkdir test-folder")	#Testing more than 1 commands in the same like like shell
    
