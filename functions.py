import pymongo
from pymongo import MongoClient
from datetime import datetime


client = MongoClient()
database = client.get_database('database')


def collection_find(
        collection: pymongo.collection.Collection,
        data: dict
) -> pymongo.cursor.Cursor:
    '''
    Выборка информации из коллекции по датам
    '''
    return collection.find({
        "dt": {
            "$gte": datetime.fromisoformat(data["dt_from"]),
            "$lte": datetime.fromisoformat(data["dt_upto"])
        }
    })


def agregation(data: dict, group_type: str) -> dict:
    '''
    Агрегация
    '''
    result = dict()
    dataset = list()
    labels = list()

    if group_type == 'month':
        for dict_ in data:
            date_ = datetime(
                year=dict_['dt'].year,
                month=dict_['dt'].month,
                day=1
            ).isoformat()
            result.setdefault(date_, []).append(dict_['value'])

    elif group_type == 'day':
        for dict_ in data:
            date_ = datetime(
                year=dict_['dt'].year,
                month=dict_['dt'].month,
                day=dict_['dt'].day
            ).isoformat()
            result.setdefault(date_, []).append(dict_['value'])

    elif group_type == 'hour':
        for dict_ in data:
            date_ = datetime(
                year=dict_['dt'].year,
                month=dict_['dt'].month,
                day=dict_['dt'].day,
                hour=dict_['dt'].hour
            ).isoformat()
            result.setdefault(date_, []).append(dict_['value'])

    [dataset.append(sum(value_)) for value_ in result.values()]
    [labels.append(key_) for key_ in result.keys()]

    return {
        "dataset": dataset,
        "labels": labels
    }
