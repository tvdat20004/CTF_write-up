from tqdm import trange
from hashlib import sha256
from Crypto.Util.number import *
out = bytes.fromhex("431b36f2b16be7471a7cce44b22a6d9d4be6faf0a6f4e5f068a6124b951826a9203d2b8bb76ee0b264447f6402baf4973c3cb365ba8e523a9c66fea5fde14b97e124adcce1fb2f88e1ea799c3d0820845ed343e6c739e54131fcb3a56e4bc1bdfbb43c052acf1843ddace6cdf93f727a96bd8dd30a70ba93ba9a339feb4183e3744ce8551ef5b3e7e167f9daadaaf27327890c1ae529771d5637ecf70550dbf90fbfe4a64372de3a802726e99b203126dadea904684f9a18f1513d24e955a819724b37bcf910ce0504f0b4ae3182d4b5c98e65aa937eeb95985d426c8ac767310fbfe4a64372de3a802726e99b203126dadea904684f9a18f1513d24e955a819c4bba1914e2444a5051c12903e945fa6e83072eabb34ec29ebab9d2442c1ac91e124adcce1fb2f88e1ea799c3d0820845ed343e6c739e54131fcb3a56e4bc1bd60265ce34d3615c52287c9c754f0be4a387e2f3e4d2aa98d40bf9d87a471c5c8a52d159f262b2c6ddb724a61840befc36eb30c88877a4030b65cbe86298449c9a52d159f262b2c6ddb724a61840befc36eb30c88877a4030b65cbe86298449c9431b36f2b16be7471a7cce44b22a6d9d4be6faf0a6f4e5f068a6124b951826a9724b37bcf910ce0504f0b4ae3182d4b5c98e65aa937eeb95985d426c8ac767318c7c63965c8cf2723dd4c9dbe9759081eb549ba822ad4553f2ae478396bbcbe96787110547bc3eda3b42ccf5854d43a57d5f4e9de110c6bd96047a921d8077043b205fbd6113316438f3771b2a12b833eb306f1c04aee3c4a9596dffd81f5903d81a65c1de02e17d9cfd88d68a8768fd1e3262f5e2fb859382fe33734b3f3ca8431b36f2b16be7471a7cce44b22a6d9d4be6faf0a6f4e5f068a6124b951826a9ca5ba87c93d42f8a45c1e0f569bba8bac92c80f4ce6c864bd44d136572411b7eba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ada52d159f262b2c6ddb724a61840befc36eb30c88877a4030b65cbe86298449c960265ce34d3615c52287c9c754f0be4a387e2f3e4d2aa98d40bf9d87a471c5c86787110547bc3eda3b42ccf5854d43a57d5f4e9de110c6bd96047a921d8077040fbfe4a64372de3a802726e99b203126dadea904684f9a18f1513d24e955a8190fbfe4a64372de3a802726e99b203126dadea904684f9a18f1513d24e955a8193b205fbd6113316438f3771b2a12b833eb306f1c04aee3c4a9596dffd81f5903431b36f2b16be7471a7cce44b22a6d9d4be6faf0a6f4e5f068a6124b951826a9498867a250a343479dddb42d5e86fcb243d037162d10d31e266ca5d3525015ee431b36f2b16be7471a7cce44b22a6d9d4be6faf0a6f4e5f068a6124b951826a9724b37bcf910ce0504f0b4ae3182d4b5c98e65aa937eeb95985d426c8ac76731a52d159f262b2c6ddb724a61840befc36eb30c88877a4030b65cbe86298449c96ae68547c7654260aa6ce171eb6bea74b9ea8f0dab1a24507a68d6595ff44fdd3b205fbd6113316438f3771b2a12b833eb306f1c04aee3c4a9596dffd81f5903431b36f2b16be7471a7cce44b22a6d9d4be6faf0a6f4e5f068a6124b951826a9431b36f2b16be7471a7cce44b22a6d9d4be6faf0a6f4e5f068a6124b951826a9c80591b73ca201ee85fa1c8a9fab735254c3f87985f9f4fc90e2809395f5f567")
chunks = [out[i:i+32] for i in range(0, len(out), 32)]
for KEY in trange(0, 256**2):
	flag = b''
	isBreak = 0
	for c in chunks:
		for b in range(32, 127):
			if sha256(long_to_bytes(KEY) + bytes([b])).digest() == c:
				flag += bytes([b])
		if not len(flag):
			break

	if len(flag):
		print(flag)