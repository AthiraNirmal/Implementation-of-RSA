
import socket
import ssl
import sys
from iplookup import iplookup
from cryptography.fernet import Fernet
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

hostname = sys.argv[1]
ip_addr = socket.gethostbyname(hostname)

key = Fernet.generate_key()
symmetric_key = Fernet(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip_addr, int(sys.argv[2])))


pcorrect='0'
inp='1'
while(pcorrect == '0'):
    
    pubKey = RSA.importKey(s.recv(2048), passphrase=None) 
    username = input(" Enter username:")
    passwd = input(" Enter password:")

    encryptor = PKCS1_OAEP.new(pubKey)
    encryptKey = encryptor.encrypt(key)

    encryptUser = symmetric_key.encrypt(username.encode())
    encryptPass = symmetric_key.encrypt(passwd.encode())

    s.send(encryptKey)
    time.sleep(1)
    # print(encryptUser)
    s.send(encryptUser)
    time.sleep(1)
    s.send(encryptPass)
    # print(encryptPass)

    pcorrect= s.recv(1024)
    pcorrect=pcorrect.decode()
    # print(pcorrect)
    if(pcorrect == '1'):
        balance = s.recv(1024)
        balance = balance.decode()
        print("Your account balance is: $",balance)
        while(inp=='1'):
            inp = input("Please select one of the following actions: \n1. Transfer\n2. Exit\n")
            if(inp == '1'):
                s.send(inp.encode())
                tranfTo= input("Enter the userid to which money needs to be transferred:\n")
                s.send(tranfTo.encode())
                amount = input("Enter the amount to transfer: ")
                s.send(amount.encode())
                newAmount = s.recv(1024)
                newAmount = newAmount.decode()

                update = s.recv(1024)
                update = update.decode()
                if(update=='1'):
                    print("Your transaction is successful")
                    print("Your balance is : $",newAmount)
                else:
                    print("Your transaction is unsuccessful")
                    print("Your balance is : $",balance)
            else:
                s.send(inp.encode())

    else:
        print("Incorrect username/password")
        pcorrect='0'
        
s.close()
