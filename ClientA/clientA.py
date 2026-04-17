import socket 
import rsa
from keygen_A import private_key, public_key, signature, aes_key
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 192.168.68.107 - Client B

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
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

public_key_B = None

def start(): 
    s.listen() 
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    conn, addr = s.accept()     # Waiting for a connection; blocking
    print(f"Connected by {addr}")
    
    ready = False
    
    while True: 
        # Receive message 
        msg_B = conn.recv(2048)
        if not msg_B:
            print("ENDING CONNECTION")
            break 
        
        elif ready:
            text = receive_msg(msg_B, aes_key)
            print(f"[CLIENT B] {text}")
            
        elif msg_B.decode(FORMAT) == "exit":
            print("ENDING CONNECTION")
            break 
        
        else:
            decoded_msg = msg_B.decode(FORMAT)
            print(f"[CLIENT B] {decoded_msg}")
    
        # Send message
        msg_A = input("Reply: ")
        
        if ready:
            send_msg(conn, msg_A, aes_key)
        
        elif msg_A == "/rsa": 
            conn.send(public_key.save_pkcs1('PEM'))
            print("RSA Key sent. Waiting for Client B's response...")
            
            public_key_B = conn.recv(2048)
            public_key_B = rsa.PublicKey.load_pkcs1(public_key_B)
            print("Received Client B's public key.")
            
        elif msg_A == "/aes":
            encrypted_aes_key = rsa.encrypt(aes_key, public_key_B) 
            header = b'key'
            conn.send(header + encrypted_aes_key + signature)
            print("Secret shared key sent. Waitng for Client B's response...")     
            
            
            msg_B = conn.recv(2048).decode(FORMAT)
            print(f"[CLIENT B] {msg_B}")
            ready = True 
            
        else: 
            conn.send(msg_A.encode(FORMAT))
    
    conn.close()
        

start()
