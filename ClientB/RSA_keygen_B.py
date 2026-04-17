import rsa 

# Generate RSA key pair once. 
# public_key, private_key = rsa.newkeys(2048)
# with open('publicB.pem', 'wb') as f: 
#     f.write(public_key.save_pkcs1('PEM'))
# with open('privateB.pem', 'wb') as f: 
#     f.write(private_key.save_pkcs1('PEM'))

with open("publicB.pem", "rb") as f: 
    public_key = rsa.PublicKey.load_pkcs1(f.read())
with open("privateB.pem", "rb") as f: 
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# msg = "Hello world"
# encrypted_msg = rsa.encrypt(msg.encode(), public_key)
# print(encrypted_msg, msg)