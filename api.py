from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.name

db.create_all()

parser = reqparse.RequestParser()
parser.add_argument('name')

class ItemList(Resource):
    def get(self):
        return {'items': [str(item) for item in Item.query.all()]}

    def post(self):
        args = parser.parse_args()
        item = Item(name=args['name'])
        db.session.add(item)
        db.session.commit()
        return {'item': str(item)}, 201

class ItemResource(Resource):
    def get(self, item_id):
        item = Item.query.get(item_id)
        if item:
            return {'item': str(item)}
        else:
            return {"error": "Item not found"}, 404

    def delete(self, item_id):
        item = Item.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {'result': True}
        else:
            return {"error": "Item not found"}, 404

api.add_resource(ItemList, '/api/items')
api.add_resource(ItemResource, '/api/items/<item_id>')

if __name__ == '__main__':
    app.run(debug=True)
