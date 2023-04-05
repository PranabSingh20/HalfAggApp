import argparse, json, string, random, time, hashlib
from schnorr_lib import n, G, bytes_from_hex, int_from_hex, sha256, point_mul, xor_bytes, bytes_from_int, tagged_hash, get_aux_rand, int_from_bytes, bytes_from_point

def get_message(): 
    # file = ".\input3.pdf" # Location of the file (can be set a different way)
    # BLOCK_SIZE = 64 # The size of each read from the file

    # file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    # with open(file, 'rb') as f: # Open the file to read it's bytes
    #     fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
    #     while len(fb) > 0: # While there is still data being read from the file
    #         file_hash.update(fb) # Update the hash
    #         fb = f.read(BLOCK_SIZE) # Read the next block from the file

    # print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash

    # return file_hash.hexdigest()

    length = 5
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Generate Schnorr signature
def schnorr_sign(messages: str, secretKey: str) -> bytes:
    msg = bytes_from_hex(messages)
    sk = secretKey
    k0 = int_from_hex(sk)
    P = point_mul(G, k0)
    assert P is not None
    k = k0 if (P[1] % 2 == 0) else n - k0
    t = xor_bytes(bytes_from_int(k), tagged_hash("BIP0340/aux", get_aux_rand()))
    z0 = int_from_bytes(tagged_hash("BIP0340/nonce", t + bytes_from_point(P) + msg)) % n
    if z0 == 0:
        raise RuntimeError()
    R = point_mul(G, z0)
    assert R is not None
    z = n - z0 if not (R[1] % 2 == 0) else z0
    hash = int_from_bytes(tagged_hash("BIP0340/challenge", bytes_from_point(R) + bytes_from_point(P) + msg)) % n
    # print("s : ", bytes_from_int((z + hash * k) % n).hex())
    sig = bytes_from_point(R) + bytes_from_int((z + hash * k) % n)
    return sig

def main():
    parser = argparse.ArgumentParser(
        description='returns the signature and the public key from a private key and a message')
    parser.add_argument('-m', '--message', type=str, help='Message to be signed')
    parser.add_argument('-sk', "--secret_key", type=str, required=True, help='Secret key of the user')
    args = parser.parse_args()
    msg = args.message
    sk = args.secret_key
    if(msg == None):
        msg = ""

    secretKey = sk


    signature = schnorr_sign(msg, secretKey)  

    signature = signature.hex()


    f = open('signatures.json')
    signatures = json.load(f)
    f.close()
    signatures.append(signature)

    json_object2 = json.dumps(signatures, indent=4)

    with open("signatures.json", "w") as f:
        f.write(json_object2)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\n\nSigning finished in %s seconds\n\n" % (time.time() - start_time))
