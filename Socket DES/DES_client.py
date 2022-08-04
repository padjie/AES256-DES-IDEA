# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:34:02 2022

@author: QNATJR
"""
from Crypto.Cipher import DES3
from hashlib import md5
import socket
import tqdm
import os
from time import process_time
from datetime import datetime



def encrypt(filename):
    file_path = "enc"+filename
    key = 'kelompok1'
    key_hash = md5(key.encode('ascii')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key,DES3.MODE_EAX,nonce=b'0')
    with open(filename, 'rb') as input_file:
        file_bytes = input_file.read()
        #Encrypt
        new_file_bytes = cipher.encrypt(file_bytes)
        with open("file/" + file_path, 'wb') as output_file:
            output_file.write(new_file_bytes)
            print(new_file_bytes)


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "192.168.0.108"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make surse it exists

# print(filename_ori)

print("Encrypting File ......")
now = datetime.now()
current_time = now.strftime("%d/%m/%y %H:%M")
print("Current Time =", current_time)
t1_start = process_time()

#key
encrypt('private.jpg')

t1_stop = process_time()
print("Elapsed time in seconds:", t1_stop-t1_start) 
print("File Encrypted")
print("\n")
# send data
filename = "file/encprivate.jpg"

# get the file size
filesize = os.path.getsize(filename)

# create the client socket
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()