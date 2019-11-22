from pymongo import MongoClient
from pprint import pprint
from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from bson import ObjectId
import json

app = Flask(__name__, static_url_path="")
api = Api(app)

client = MongoClient("mongodb://localhost:27017/")

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
	'uri': fields.Url('task')
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
		print("HGHFJHGJHG")
		print(self.reqparse.parse_args())
		print("gsdhgfskjhgdfj")
		return "dasd", 201
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
		task = [task for task in tasks if task['id'] == id]
		if len(task) == 0:
			abort(404)
		return {'task': marshal(task[0], task_fields)}

	def put(self, id):
		task = [task for task in tasks if task['id'] == id]
		if len(task) == 0:
			abort(404)
		task = task[0]
		args = self.reqparse.parse_args()
		for k, v in args.items():
			if v is not None:
				task[k] = v
		return {'task': marshal(task, task_fields)}

	def delete(self, id):
		task = [task for task in tasks if task['id'] == id]
		if len(task) == 0:
			abort(404)
		tasks.remove(task[0])
		return {'result': True}


class HealthCheck(Resource):
	def get(self):
		return "OK"

api.add_resource(TaskListAPI, '/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint='task')
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