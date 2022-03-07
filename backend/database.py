import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.Items
collection = database.Item


async def fetch_result(input):
    result = await collection.find_one({"input": input})
    return result


async def add_result(output):
    document = output
    result = await collection.insert_one({output})
    return document
