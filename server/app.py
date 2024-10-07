from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Earthquake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    earthquake = db.session.get(Earthquake, id)

    earthquakes_dict = [quake.to_dict() for quake in earthquake]
    return make_response(jsonify(earthquakes_dict), 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return make_response(earthquake.to_dict(), 200)
    else:
        return make_response({'message': f'Earthquake {id} not found.'}, 404)

@app.route('/earthquakes/<int:id>', methods=['DELETE'])
def delete_earthquake(id):
    earthquake = db.session.get(Earthquake, id)

    if earthquake:
        db.session.delete(earthquake)
        db.session.commit()
        return make_response(jsonify({'message': 'Earthquake deleted successfully'}), 200)
    else:
        return make_response(jsonify({'error': 'Earthquake not found'}), 404)
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    response_data = {
        "count": len(earthquakes),  # Number of earthquakes found
        "quakes": [eq.to_dict() for eq in earthquakes]  # List of earthquake data
    }
    
    # Return 200 OK regardless of whether we found matches or not
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
