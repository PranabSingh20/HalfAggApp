import os, json
from typing import Tuple
import time


from schnorr_lib import bytes_from_int,n, p, G, bytes_from_point, point_mul

Point = Tuple[int, int]
timetaken = 0

def create_keypair(n_keys: int):
    global timetaken
    keyPairs = []
    # Generate n keys
    for i in range(0, n_keys):
        privkey = os.urandom(32)
        privkey_int = int(privkey.hex(), 16) % n
        cur = time.time()
        publickey = point_mul(G, privkey_int)
        timetaken += (time.time()-cur)

        privkey_even = privkey_int if (publickey[1] % 2 == 0) else n - privkey_int
        hex_privkey = hex(privkey_even).replace('0x', '').rjust(64, '0')
        keyPairs.append([
            hex_privkey,
            bytes_from_point(publickey).hex()
        ])
    return keyPairs


def keypairs(): 
    n_keys = 1

    keyPairs = create_keypair(n_keys)

    f = open('publickeys.json')
    publickeys = json.load(f)
    f.close()

    publickeys.append(keyPairs[0][1])
    json_object1 = json.dumps(publickeys, indent=4)
    with open("publickeys.json", "w") as f:
        f.write(json_object1)
    return keyPairs[0][0]


if __name__ == "__main__":
    start_time = time.time()
    keypairs()
    # print("Time taken for point mul ", timetaken)
    print("\n\nKeyGen finished in %s seconds\n\n" % (time.time() - start_time))
    # extra = time.time()
    # x = os.urandom(32)
    # x = int(x.hex(), 16) % n
    # for i in range(256*100):
    #     y = pow(x, p-2, p)
    # print("\n\nExtra time %s seconds " % (time.time() - extra))