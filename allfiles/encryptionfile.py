from cryptography.fernet import Fernet

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()

#print(load_key())


def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    #print(encrypted_message)
    #print(type(encrypted_message))
    return str(encrypted_message,'utf-8')

#password = encrypt_message(message)
#print(type(password))
#a = str(password,'utf-8')
#print(a)

def decrypt_message(msg):
    """
    Decrypts an encrypted message
    """
    encrypted_message = bytes(msg,'utf-8')
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return (decrypted_message.decode())
#decrypt_message(i[0])

