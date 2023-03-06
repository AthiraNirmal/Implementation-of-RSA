import socket, ssl
import sys
import subprocess
import threading 
import rsa
from cryptography.fernet import Fernet

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

import hashlib
import fileinput

keyPair = RSA.generate(3072)
pubKey = keyPair.publickey()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', int(sys.argv[1])))
while True:
    s.listen(1)
    newsocket, fromaddr = s.accept()

    myvars = {}
    with open("balance.txt") as f1:
        for line in f1:
            userid, balance = line.partition(" ")[::2]
            myvars[userid.strip()] = balance

    conn=1
    while(conn ==1):
        newsocket.send(keyPair.publickey().exportKey(format='PEM', passphrase=None, pkcs=1)) 
        # encryptKey = importKey(s.recv(2048), passphrase=None) 

        encryptKey = newsocket.recv(2048)
        encryptUser = newsocket.recv(2048)
        encryptPasswd = newsocket.recv(2048)
        decryptor = PKCS1_OAEP.new(keyPair)
        key = decryptor.decrypt(encryptKey)


        key= Fernet(key)
        username  = key.decrypt(encryptUser)
        passwd = key.decrypt(encryptPasswd)
        print(username)
        print(passwd)

        f = open("passwd.txt", "r")
        for x in f:
            # username = username.decode()
            if(username.decode() in x):
                hashPass = hashlib.md5(passwd).hexdigest()
                if(hashPass in x):
                    code = '1'
                    newsocket.send(code.encode())
                    print("correct password")
                    balance = myvars[username.decode()]
                    newsocket.send(balance.encode())
                    while(newsocket.recv(1024).decode()=='1'):
                        tranfTo= newsocket.recv(1024).decode()
                        print(tranfTo)
                        amount=newsocket.recv(1024).decode()
                        print(amount)
                        bal = int(balance)
                        amt = int(amount)
                        if(bal >= amt):
                            newAmt = bal-amt
                            myvars[username.decode()] = str(newAmt)
                            newTransAmt = int(myvars[tranfTo])+amt
                            myvars[tranfTo]  = str(newTransAmt)
                            newsocket.send(str(newAmt).encode())
                            with open("balance.txt", 'w') as f: 
                                for key, value in myvars.items(): 
                                    f.write('%s %s\n' % (key, value))
                            transUpdate = '1'
                            newsocket.send(transUpdate.encode())
                        else:
                            transUpdate = '0'
                            newsocket.send(transUpdate.encode())
                    # conn =0
                    # else:
                    conn=0
                    
                else:
                    code = '0'
                    newsocket.send(code.encode())

                


    








    
