from challenge.cryptoutil import *
# from challenge.util import *
cookie = "user_id=guest&isLoggedIn=False.4a8863f4dcf32d63048febabb24cf36552f392cff027a5de143785a7af85ebd8"

data, hash = cookie.split(".")
appended_data = b"&isLoggedIn=True"
new_data = pad(pad(b'0'*50 + data.encode()) + appended_data)
blocks = [new_data[i:i+32] for i in range(0, len(new_data), 32)]

hash = bytes.fromhex(hash)

new_hash = compression_function(blocks[-1], hash)
new_data = pad(b'0'*50 + data.encode()) + appended_data
payload = "{}.{}".format(new_data[50:].decode(), new_hash.hex())
print(payload)