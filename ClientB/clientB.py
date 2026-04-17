import socket
import rsa 
from RSA_keygen_B import private_key, public_key
from Crypto.Hash import SHA256

PORT = 5050
FORMAT = 'utf-8'
SERVER = input("Please enter the IP Address: ")       # 192.168.68.106
ADDR = (SERVER, PORT)

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(ADDR)

public_key_A = None 
aes_key = None


while True: 
    # Send message 
    msg = input("Reply: ")
    c.send(msg.encode(FORMAT))

    # Receive message
    msg_A = c.recv(2048)
    if not msg_A or msg_A.decode(FORMAT) == 'exit':
        print(f"ENDING CONNECTION.")
        break

    elif b"-----BEGIN RSA PUBLIC KEY-----" in msg_A:
        print("\nRSA Public Key received from Client A.")
        public_key_A = rsa.PublicKey.load_pkcs1(msg_A)

        c.send(public_key.save_pkcs1('PEM'))
        print("RSA Public Key sent.")

    elif msg_A.decode(FORMAT) == "secret_key": 
        cipher = c.recv(2048)
        
        aes_key = cipher[:256]
        aes_key = rsa.decrypt(aes_key, private_key)
        sign = cipher[256:]

        try:
            rsa.verify(aes_key, sign, public_key_A)
            print("Secret key received!")
            c.send("Secret key received!".encode())

        except rsa.VerificationError:
            print("Invalid secret key.")
            break 
    else:
        print(f"[CLIENT A] {msg_A.decode(FORMAT)}") 

