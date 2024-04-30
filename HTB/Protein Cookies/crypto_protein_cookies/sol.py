import hashlib, base64, os
from urllib.parse import parse_qs
import HashTools
cookie = "dXNlcm5hbWU9Z3Vlc3QmaXNMb2dnZWRJbj1GYWxzZQ==.MzU3ZWM1Y2EzZThjNjZkZWY3ZjYwZmQ3MjZlODNlZmUwNzY3OTNjNTIyMWVjM2YwM2U2ODIyOGY0ZmQwYzM5NzI3M2ZkNGNkYTcyMjRhYjI0Njg2ZjdhMTlkYTRlZmI3MzQ0ZjU2ZDA5YzhkZmFmNzEyM2VjMjE3OGQwNDhiOGQ="

hash_input, hash = map(base64.b64decode, cookie.split('.'))
# secret = os.urandom(16)
secret = b"1111111111111111"

hash = hash.decode()
class session:
    @staticmethod
    def create(username, logged_in='True'):
        if username == 'guest':
            logged_in = 'False'

        hashing_input = 'username={}&isLoggedIn={}'.format(username, logged_in)
        crypto_segment = signature.create(hashing_input.encode())
        
        return '{}.{}'.format(signature.encode(hashing_input), crypto_segment)

    @staticmethod
    def validate_login(payload):
        hashing_input, crypto_segment = payload.split('.')

        if signature.integrity(hashing_input, crypto_segment):
            return {
                k: v[-1] for k, v in parse_qs(signature.decode(hashing_input)).items()
            }.get('isLoggedIn', '') == 'True'
        
        return False

class signature:
    @staticmethod
    def encode(data):
        return base64.b64encode(data.encode()).decode()

    @staticmethod
    def decode(data):
        return base64.b64decode(data.encode())

    @staticmethod
    def create(payload : bytes, secret=secret):
        return signature.encode(hashlib.sha512(secret + payload).hexdigest())
    
    @staticmethod
    def integrity(hashing_input, crypto_segment):
        return signature.create(signature.decode(hashing_input)) == crypto_segment
# payload = hash_input + "&isLoggedIn=True"
# payload = signature.encode(payload) + "." + signature.create(payload.encode())
appended_data = b"&isLoggedIn=True"
attack = HashTools.new("sha512")
new_data, new_hash = attack.extension(secret_length=16, original_data=hash_input, append_data=appended_data, signature=hash)
print(new_data, new_hash)
print("{}.{}".format(base64.b64encode(new_data).decode(), base64.b64encode(new_hash.encode()).decode()))