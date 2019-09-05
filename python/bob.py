import bb84
import json
import base64
import os
import time

n = 128
key_length = 10

while not os.path.exists('ids'):
    time.sleep(1)

idsfile = open('ids', 'r')
ids = json.loads(base64.b64decode(idsfile.read()))
idsfile.close()

bits, arrows = bb84.dissolveQbits(ids, bb84.measureQbitsOnline)
if bits == None:
    raise Exception("Qbits escaped.")

arrowsfile = open('arrows_bob', 'w')
arrowsfile.write(base64.b64encode(bytes(json.dumps(arrows), 'utf-8')).decode())
arrowsfile.close()

while not os.path.exists('diff'):
    time.sleep(1)

arrowsalicefile = open('diff', 'r')
diff = json.loads(base64.b64decode(arrowsalicefile.read()))
arrowsalicefile.close()

key = bb84.discard(bits, diff)

os.remove('ids')
os.remove('diff')

print("Bob's Key: " + hex(int(''.join([ str(i) for i in key ]), 2))[2:key_length + 2])
