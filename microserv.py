from pymongo import MongoClient
from pprint import pprint
from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from bson import ObjectId, json_util
import bson
import json
import sys

if len(sys.argv) > 1:
    public_ip = str(sys.argv[1])


app = Flask(__name__, static_url_path="")
api = Api(app)

client = MongoClient("mongodb://"+public_ip+":27017/")

db = client["cloud"]

collection = db["col"]

tasks = [
	{
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
		'done': False
	},
	{
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web',
		'done': False
	}
]

task_fields = {
	'title': fields.String,
	'description': fields.String,
	'done': fields.Boolean,
	'uri': fields.Url('tasks')
}

def parser_find(res):
	return {
		"_id": str(res["_id"]),
		"description": res["description"],
		"done": res["done"],
		"title": res["title"]
	}

class TaskListAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str, required=True,
								   help='No task title provided',
								   location='json')
		self.reqparse.add_argument('description', type=str, default="",
								   location='json')
		super(TaskListAPI, self).__init__()

	def get(self):
		l_ret = []
		for x in collection.find():
			l_ret.append(parser_find(x))
		return {'tasks': l_ret}

	def post(self):
		args = self.reqparse.parse_args()
		task = {
			'title': args['title'],
			'description': args['description'],
			'done': False
		}

		collection.insert_one(task)
		
		return {'task': marshal(task, task_fields)}, 201

class TaskAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str, location='json')
		self.reqparse.add_argument('description', type=str, location='json')
		self.reqparse.add_argument('done', type=bool, location='json')
		super(TaskAPI, self).__init__()

	def get(self, id):
		try:
			x = collection.find_one({"_id": ObjectId(id)})
		except bson.errors.InvalidId as e:
			return "Formato de Id incorreto"
		if x is None:
			return "Nao existe task com o id \'{}\'".format(id)
		return parser_find(x)

	def put(self, id):
		try:
			object_id = ObjectId(id)
		except bson.errors.InvalidId as e:
			return "Formato de Id incorreto"
		x = collection.find_one({"_id": object_id})
		if x is None:
			return "Nao existe task com o id \'{}\'".format(id)

		args = self.reqparse.parse_args()

		task = {
			'title': args['title'],
			'description': args['description'],
			'done': args["done"]
		}

		collection.update_one({'_id': ObjectId(id)},
					{'$set':task}, upsert=False)
		return {'task': marshal(task, task_fields)}

	def delete(self, id):
		try:
			object_id = ObjectId(id)
		except bson.errors.InvalidId as e:
			return "Formato de Id incorreto"
		x = collection.find_one({"_id": object_id})
		if x is None:
			return "Nao existe task com o id \'{}\'".format(id)

		collection.delete_one({"_id": object_id})
		return {'result': True}


class HealthCheck(Resource):
	def get(self):
		return "OK"

api.add_resource(TaskListAPI, '/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/tasks/<id>', endpoint='task')
api.add_resource(HealthCheck, "/healthcheck", endpoint="healthcheck")

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port=5000)



#mydict = { "name": "John", "address": "Highway 40" }
'''
x = collection.insert_many(tasks)
print("insert")

print("find1")
x = collection.find()

for x in collection.find():
  pprint(x)

myquery = { "address": "Highway 40" }
print("delete")
collection.delete_many(myquery)

print("find2")
x = collection.find()

for x in collection.find():
  pprint(x)
'''