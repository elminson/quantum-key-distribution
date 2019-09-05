import secrets
import requests
localQbits = {}

def split_list(alist, parts=1):
    if parts < 1: parts = 1
    length = len(alist)
    return [ alist[i*length // parts: (i+1)*length // parts] 
             for i in range(parts) ]

def uploadQbitsOnline(qbits):
    for parts in split_list(qbits, int(len(qbits) / 128)):
        resp = requests.put("https://quantum.ludlows.org/channel", json=parts).json()
        if 'message' in resp: return False
    return True 

def measureQbitsOnline(measure):
    result = []
    for parts in split_list(measure, int(len(measure) / 128)):
        resp = requests.post("https://quantum.ludlows.org/channel", json=parts).json()
        if 'message' in resp: return None
        result += resp
    return result

def uploadQbit(qbit):
    localQbits[qbit['id']] = qbit
    return True

def uploadQbits(qbits):
    [uploadQbit(qbit) for qbit in qbits]
    return True

def measureQbit(qbit, arrow):
    if qbit == None:
        return qbit
    if arrow == qbit['arrow']:
        return qbit['bit']
    if arrow != qbit['arrow']:
        return secrets.choice([1, 0])

def measureQbits(request):
    return [
        measureQbit(
            localQbits.pop(unit['id']) 
            if unit['id'] in localQbits else None,
            unit['arrow']
        )
        for unit in request
    ]

def dissolveQbits(ids, measureFunc=measureQbits):
    arrows = [ secrets.choice([1, 0]) for id in ids ]
    measure = [
        {
            'id': id,
            'arrow': unit % 2
        }
        for id, unit in zip(ids, arrows)
    ]
    return measureFunc(measure), arrows

def requestQbits(length, uploadFunc=uploadQbits):
    import uuid

    bits = [ secrets.choice([1, 0]) for i in range(length) ]
    arrows = [ secrets.choice([1, 0]) for i in range(length) ]

    qbits = [
        {
            'id': str(uuid.uuid4()),
            'bit': bit,
            'arrow': arrow
        }
        for bit, arrow in zip(bits, arrows)
    ]

    ids = [ qbit['id'] for qbit in qbits ]
    return ids if uploadFunc(qbits) else None, bits, arrows 

diff = lambda a, b: [  i == j for i, j in zip(a, b) ]
discard = lambda sequence, diff: list(
    filter(
        lambda i:  i in [0, 1], 
        [ i if same else None for i, same in zip(sequence, diff) ]
    )
)
