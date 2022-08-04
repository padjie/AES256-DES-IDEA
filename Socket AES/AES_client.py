# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:34:02 2022

@author: QNATJR
"""
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
import socket
import tqdm
import os
from time import process_time
from datetime import datetime

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = "enc"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:#rb means read in binary
		with open("file/" + outputFile, 'wb') as outfile:#wb means write in the binary mode
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk)%16 != 0:
					chunk += b' '*(16-(len(chunk)%16))

				outfile.write(encryptor.encrypt(chunk))

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

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
encrypt(getKey('kelompok1'), 'public.txt')

t1_stop = process_time()
print("Elapsed time in seconds:", t1_stop-t1_start) 
print("File Encrypted")
print("\n")
# send data
filename = "file/encpublic.txt"

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