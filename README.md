## Encrypted Chat System
Python-based encrypted chat application that uses RSA to share AES-256 (CBC mode) key for secure, encrypted communication between two clients.

## Prerequisites:
- Python 3
- pip install pycryptodome rsa

## Procedure
1. Ensure that the clients have their respective folders, containing keygen, and the main python files.
2. Run ClientA.py and ClientB.py - in separate machines.
3. Obtain the IP address of Client A and enter it in the prompt of ClientB.
4. To exchange the public keys, simply type /rsa from ClientA.
5. To exchange the shared secret key, type /aes again from ClientA.
6. And done! All the following messages will be encrypted!
