# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:32:36 2022

@author: QNATJR
"""
from Crypto.Cipher import DES3
from hashlib import md5
import socket
import tqdm
import os
from time import process_time
from datetime import datetime

def decrypt(filename):
    file_path = "dec"+filename[3:]
    key = 'kelompok1'
    key_hash = md5(key.encode('ascii')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key,DES3.MODE_EAX,nonce=b'0')
    with open(filename, 'rb') as input_file:
        file_bytes = input_file.read()
        #Encrypt
        new_file_bytes = cipher.decrypt(file_bytes)
        with open("file/" + file_path, 'wb') as output_file:
            output_file.write(new_file_bytes)
            print(new_file_bytes)

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()


#startting time
now = datetime.now()
current_time = now.strftime("%d/%m/%y %H:%M")

print("\n")
print("Decrypting File ......")
print("Current Time =", current_time)

t1_start = process_time()
decrypt('encprivate.jpg')
t1_stop = process_time()
print("Elapsed time in seconds:", t1_stop-t1_start)
print("File Decrypted")
print("\n")


os.remove("encprivate.jpg")