#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def getPlant(self):
        plant_dict=[p.to_dict() for p in  Plant.query.all()]
        return jsonify({"data":plant_dict})

class PlantByID(Resource):
    def getPlantById(self,id):
        plant_dict=Plant.query.filter_by(id=int(id)).first().to_dict()
        if  not plant_dict:
            return jsonify({'message': 'Plant not found'}), 404
        else:
            return jsonify(plant_dict),200
        
api.add_resource(PlantByID,'/plants/<int:id>')
        
class PlantPost(Resource):
    def post(self):
        new_plant=Plant(
            name=request.form["name"],
            image=request.form["image"],
            price=request.form["price"],
        )
        db.session.add(new_plant)
        db.session.commit()
        plant_list_dict=new_plant.to_dict()
        return jsonify(plant_list_dict),200
    
api.add_resource(PlantPost,'/plants')
        
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
