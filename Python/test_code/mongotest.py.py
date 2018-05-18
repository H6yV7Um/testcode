#-*-coding:utf-8 -*-
import pymongo
from datetime import datetime

print "------------------------connection---------------------------"
host = "123.56.26.7"
port = 27017
#uri = 'mongodb://user:passwd@host/my_database'
uri = 'mongodb://test:123456@123.56.26.7/test'
#client = pymongo.MongoClient(host=host,port=port)   #host和port连接方式，支持list：[(host,port),(host,port)]
client = pymongo.MongoClient(uri)      #uri连接方式
db = client.test    #连接数据库test
print db
print "------------------------insert----------------------------"
result1 = db.testset.insert_one(    #往集合testset中插入单条数据，集合相当于RDB中的table
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        }
    }
)
result2 = db.testset.insert_many([      #以list形式插入多条数据
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        }
    },
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266],
            "master":"yinzhixin"
        }
    },
     {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": 1480,
            "coord": [-73.9557413, 40.7720266],
            "master":"hello"
        }
    }
    ]
    )
print result1
print result2
print db.collection_names(include_system_collections=True)  #输出当前数据库的所有集合
print "-----------------find---------------------"
hel = db.testset.find_one() #返回一个dict
print hel
#hels = db.testset.find()    #返回一个可迭代的cursor对象
hels = db.testset.find({"address.master":"yinzhixin"})  #添加过滤条件的查询
print "count:%s" %hels.count()
for document in hels:
    print document
table = db.testset
for document in table.find({'building':{'$lt':1500}}).sort('master'):
    print "sorted:" + document
'''
print "-----------------remove----------------"
table.remove({"address.master":"liuxiaoya"})    #条件删除
for document in table.find():
    print document
table.remove()          #删除全部
print "count:%s" %table.count()  
print "---------------update------------------"
table.update_many({"address.master":"yinzhixin"}, {"$set":{"address.master":"liuxiaoya"}})  #更新所有满足条件的
for document in table.find():
    print document
table.update({"address.master":"liuxiaoya"}, {"$set":{"address.master":"banana"}})  #更新第一条满足条件的
'''