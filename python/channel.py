def inConv(data):
    import time
    result = {
        'id': { 'S': data['id'] },
        'arrow': { 'BOOL': bool(data['arrow']) },
        'ttl': { 'N': str(int(time.time() + 60)) }
    }
    if 'bit' in data: result['bit'] = { 'BOOL': bool(data['bit']) }
    return result

def outConv(data, null):
    result = {
        'id': data['id']['S'],
        'arrow': int(data['arrow']['BOOL'])
    }
    if 'bit' in data: result['bit'] = int(data['bit']['BOOL'])
    return result

def measureQbit(qbit, arrow):
    import secrets
    if qbit == None:
        return qbit
    if arrow == qbit['arrow']:
        return qbit['bit']
    if arrow != qbit['arrow']:
        return secrets.choice([1, 0])

def func(event, context):
    import json
    import boto3

    method = event['httpMethod']
    data = json.loads(event['body'])

    client = boto3.client('dynamodb')

    result = {
        'statusCode': 200,
        'headers': {}
    }
    if method == 'PUT':
        [
            client.put_item(
                TableName='quantums',
                Item=inConv(qbit),
                ConditionExpression='attribute_not_exists(id)',
            )

            for qbit in data
        ]
        result['body'] = json.dumps({})
        return result
        
    if method == 'POST':
        data = [
            measureQbit(outConv(
                client.get_item(
                    TableName='quantums',
                    Key={
                        "id": { 'S': qbit['id'] }
                    },
                    ConsistentRead=True,
                )['Item'],
                client.delete_item(
                    TableName='quantums',
                    Key={
                        "id": { 'S': qbit['id'] }
                    }
                )
            ), qbit['arrow'])
            for qbit in data
        ]
        result['body'] = json.dumps(data)
        return result
        