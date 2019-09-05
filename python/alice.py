import bb84
import json
import base64
import os
import time

n = 128
key_length = 10

ids, bits, arrows = bb84.requestQbits(n, bb84.uploadQbitsOnline)
if ids == None:
    raise Exception("Qbits escaped.")

idsfile = open('ids', 'w')
idsfile.write(base64.b64encode(bytes(json.dumps(ids), 'utf-8')).decode())
idsfile.close()


while not os.path.exists('arrows_bob'):
    time.sleep(1)

arrowsbobfile = open('arrows_bob', 'r')
arrows_bob = json.loads(base64.b64decode(arrowsbobfile.read()))
arrowsbobfile.close()

diff = bb84.diff(arrows, arrows_bob)

difffile = open('diff', 'w')
difffile.write(base64.b64encode(bytes(json.dumps(diff), 'utf-8')).decode())
difffile.close()

key = bb84.discard(bits, diff)

os.remove('arrows_bob')

print("Alice's Key: " + hex(int(''.join([ str(i) for i in key]), 2))[2:key_length + 2])
