#!/usr/bin/env python3
"""Func gives stats on Nginx logs stored in MongoDB"""


from pymongo import MongoClient


def nginx_logs(nginx_collection):
    """Stats on Nginx request logs"""
    tl = nginx_collection.count_documents({})
    print(f'{tl} logs')

    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {req}')

    stats = nginx_collection.count_documents(
        {'method': 'GET', 'path': '/status'})
    print(f'{stats} status check')

    w_flow = [
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]
    addrss = nginx_collection.aggregate(w_flow)

    print('IPs:')
    for addr in addrss:
        print(f'\t{addr["_id"]}: {addr["count"]}')


def exec():
    """Stats on Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    nginx_logs(nginx_collection)


if __name__ == '__main__':
    exec()
