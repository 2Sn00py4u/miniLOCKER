# /// install dependencies ///
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# /// classes
def encrypting(password: str, key: str) -> bytes:           
    # /// varibles ///
    byte_password = bytes(password, "utf-8")
    byte_key = bytes(key, "utf-8")
    encryption_key = pad(byte_key, AES.block_size)
    blockdecryption = "ECB"
    
    # /// cipher
    if blockdecryption == "ECB":
        try:
            cipher = AES.new(encryption_key, AES.MODE_ECB)
        except Exception as e:
            raise Exception(f"an error accured, make shure, to use the right key\nerror:{e}")
    else:
        raise Exception("other than ECB not done yet...")
    
    try:
        padded_password = pad(byte_password, AES.block_size)
        encrypted_password = cipher.encrypt(padded_password)
        return encrypted_password
    except:
        raise Exception(f"error encrypting {byte_password}") 
  
        
def decrypting(encrypted_bytes:bytes, key:str) -> str:
    # /// varibles ///
    byte_key = bytes(key, "utf-8")
    encryption_key = pad(byte_key, AES.block_size)
    blockdecryption = "ECB"
    
    # /// cipher
    if blockdecryption == "ECB":
        try:
            cipher = AES.new(encryption_key, AES.MODE_ECB)
        except Exception as e:
            raise Exception(f"an error accured, make shure, to use the right key\nerror:{e}")
    else:
        raise Exception("other than ECB not done yet...")
    
    try:
        decrypted_password = cipher.decrypt(encrypted_bytes)
        bytetext = unpad(decrypted_password, AES.block_size)
        return bytetext.decode("utf-8")
    except:
        raise Exception(f"error decrypting {byte_key}")

def compare_encrypted(password_guess: str, key_guess: str, encrypted_password: bytes) -> bool:
    try:
        encrypted_passwordguess = encrypting(password_guess, key_guess)
        if encrypted_passwordguess == encrypted_password:
            return True
        else:
            return False
        
    except:
        return "couldn't encrypt password"
"""
print(hash:=encrypting("admin", "admin"))
print(decrypting(hash, "admin"))
print(compare_encrypted("admin", "admin", hash))"""
