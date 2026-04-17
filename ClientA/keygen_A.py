import rsa 
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

# Generate RSA key pair once Client A.
# public_key, private_key = rsa.newkeys(2048)
# with open('publicA.pem', 'wb') as f:
#     f.write(public_key.save_pkcs1('PEM')) 
# with open('privateA.pem', 'wb') as f:
#     f.write(private_key.save_pkcs1('PEM'))

with open("publicA.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
with open("privateA.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())


#===========================================

aes_key = get_random_bytes(32)
signature = rsa.sign(aes_key, private_key, 'SHA-256')


    
    
    
