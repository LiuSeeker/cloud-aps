from flask import Flask, jsonify, abort, make_response, redirect, request
from flask_restful import Api, Resource, reqparse, fields, marshal
import requests
import json
import sys

app = Flask(__name__, static_url_path="")
api = Api(app)

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

if len(sys.argv) > 1:
	public_ip = str(sys.argv[1])


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
		res = requests.get(url="http://"+public_ip+":5000/tasks")
		return res.json()

	def post(self):
		args = self.reqparse.parse_args()
		task = {
			'title': args['title'],
			'description': args['description']
		}
		print(task)
		res = requests.post(url="http://"+public_ip+":5000/tasks", json=task)
		return res.json()

class TaskAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str, location='json')
		self.reqparse.add_argument('description', type=str, location='json')
		self.reqparse.add_argument('done', type=bool, location='json')
		super(TaskAPI, self).__init__()

	def get(self, id):
		res = requests.get(url="http://"+public_ip+":5000/tasks/"+id)
		return res.json()

	def put(self, id):
		args = self.reqparse.parse_args()
		task = {
			'title': args['title'],
			'description': args['description'],
			'done': args['done']
		}
		res = requests.put(url="http://"+public_ip+":5000/tasks/"+id, json=task)
		return res.json()

	def delete(self, id):
		args = self.reqparse.parse_args()
		task = {
			'title': args['title'],
			'description': args['description'],
			'done': args['done']
		}
		res = requests.delete(url="http://"+public_ip+":5000/tasks/"+id, json=task)
		return res.json()

class HealthCheck(Resource):
	def get(self):
		res = requests.get(url="http://"+public_ip+":5000/healthcheck")
		return res.json()

api.add_resource(TaskListAPI, '/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/tasks/<id>', endpoint='task')
api.add_resource(HealthCheck, "/healthcheck", endpoint="healthcheck")


if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port=5000)
