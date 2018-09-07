import pymongo
from zhihu import settings


def query_item(url_token):
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('user')
    data = tb.find_one({'url_token': url_token})
    client.close()
    return data


def get_collect_task():
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('collect_task')
    data = tb.find_one({'status': 'INIT'})
    if data is None:
        return None
    else:
        res = dict(data)
        tb.update({'token': res['token']}, {'$set': {'status': "COLLECTING"}})
        res.pop('_id')
        return res['token']


def finish_collect_task(token):
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('collect_task')
    tb.update({'token': token}, {'$set': {'status': 'ANLAYZE_WAIT'}})
