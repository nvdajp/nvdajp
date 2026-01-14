# @param fileHash: The SHA-1 hash of the file as a hex string.
# @type fileHash: basestring

import hashlib
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("fileName")
args = ap.parse_args()

fd = open(args.fileName, "rb")
data = fd.read()
fd.close()

hasher = hashlib.sha1()
hasher.update(data)
print(args.fileName)
print("launcherHash: %s" % hasher.hexdigest())
