import socket
import rsa 
from RSA_keygen_B import private_key, public_key
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def send_msg(conn, message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    iv = cipher.iv  # random IV
    
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    conn.send(iv + ciphertext)  
    
def receive_msg(msg_B, aes_key):
    iv = msg_B[:16]  # Extract IV
    ciphertext = msg_B[16:]  # Extract ciphertext
    
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return plaintext.decode('utf-8') 

PORT = 5050
FORMAT = 'utf-8'
SERVER = input("Please enter the IP Address: ")       # 192.168.68.106
ADDR = (SERVER, PORT)

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(ADDR)

public_key_A = None 
aes_key = None
ready = False

while True: 
    # Send message 
    msg = input("Reply: ")
    if ready:
        send_msg(c, msg, aes_key)
    else:
        c.send(msg.encode(FORMAT))

    # Receive message
    msg_A = c.recv(2048)
    
    if ready:
        text = receive_msg(msg_A, aes_key)
    
    decoded_msg_A = ""
    try:
        decoded_msg_A = msg_A.decode(FORMAT)
    except UnicodeDecodeError:
        decoded_msg_A = None 
    
    if not msg_A or decoded_msg_A == 'exit':
        print(f"ENDING CONNECTION.")
        break

    elif b"-----BEGIN RSA PUBLIC KEY-----" in msg_A:
        print("\nRSA Public Key received from Client A.")
        public_key_A = rsa.PublicKey.load_pkcs1(msg_A)

        c.send(public_key.save_pkcs1('PEM'))
        print("RSA Public Key sent.")

    elif decoded_msg_A == "secret_key": 
        cipher = c.recv(2048)
        
        aes_key = cipher[:256]
        aes_key = rsa.decrypt(aes_key, private_key)
        sign = cipher[256:]

        try:
            rsa.verify(aes_key, sign, public_key_A)
            print("Secret key received!")
            c.send("Secret key received!".encode())
            ready = True

        except rsa.VerificationError:
            print("Invalid secret key.")
            break 
    else:
        print(f"[CLIENT A] {decoded_msg_A}") 
