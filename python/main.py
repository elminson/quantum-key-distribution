import bb84

n = 2048
key_length = 128
ids, bits_alice, arrows_alice = bb84.requestQbits(n)
bits_bob, arrows_bob = bb84.dissolveQbits(ids)
diff = bb84.diff(arrows_alice, arrows_bob)
key_alice = bb84.discard(bits_alice, diff)
key_bob = bb84.discard(bits_bob, diff)

print("Alice's Key: " + hex(int(''.join([ str(i) for i in key_alice]), 2))[2:key_length + 2])
print("Bob's Key: " + hex(int(''.join([ str(i) for i in key_bob]), 2))[2:key_length + 2])