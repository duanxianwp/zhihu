import pymongo
from zhihu import settings


def query_item(url_token):
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('user')
    data = tb.find_one({'url_token': url_token})
    client.close()
    return data
