from cryptography.fernet import Fernet

"""Run the lines below just once, to generate the key. Then store it safe to encode/decode as required"""
#key = Fernet.generate_key()  # store in a secure location
#print("Key:", key.decode())


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


"""Manually encrypt each variable, and store the encrypted value in the YML files as ENV Variable"""
#message = "type message"
#enc_user = encrypt(message.encode(), key)

#token = enc_user
#dec_user = decrypt(token, key).decode()

#print(enc_user)