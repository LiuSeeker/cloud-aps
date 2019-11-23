from flask import Flask, jsonify, abort, make_response, redirect, request
from flask_restful import Api, Resource, reqparse, fields, marshal
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
        return redirect("http://"+public_ip+":5000/tasks", code=302)

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'title': args['title'],
            'description': args['description']
        }
        return redirect("http://"+public_ip+":5000/tasks") ##arrumar

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        return redirect("http://"+public_ip+":5000/tasks/"+id, code=302)

    def put(self, id):
       return redirect("http://"+public_ip+":5000/tasks/"+id)##arrumar

    def delete(self, id):
        return redirect("http://"+public_ip+":5000/tasks/"+id)##arrumar

class HealthCheck(Resource):
    def get(self):
        return redirect("http://"+public_ip+":5000/healthcheck", code=302)

api.add_resource(TaskListAPI, '/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/tasks/<id>', endpoint='task')
api.add_resource(HealthCheck, "/healthcheck", endpoint="healthcheck")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
