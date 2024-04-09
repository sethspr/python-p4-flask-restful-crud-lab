#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


@app.route('/plants', methods=['GET', 'POST'])
def all_plants():
    if request.method == 'GET':
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)
    elif request.method == 'POST':
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


@app.route('/plants/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def plant_by_id(id):
    plants = Plant.query.filter_by(id=id).first()

    if plants is None:
        return {'error': f'{id} not found'}, 404

    if request.method == 'GET':
        plant_dict = plants.to_dict()
        return make_response(jsonify(plant_dict), 200)
    
    elif request.method == 'PATCH':
        json_data = request.get_json()

        for field in json_data:
            value = json_data[field]
            setattr(plants, field, value)

        db.session.commit()

        updated_plant_dict = plants.to_dict()
        return make_response(jsonify(updated_plant_dict), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(plants)
        db.session.commit()

        return {}, 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)
