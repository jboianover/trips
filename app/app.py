import os
import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from controller import trip_controller


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


# Define the endpoint to return all rows from the 'trip' table
@app.route('/trips', methods=['GET'])
def get_trips():
    if not request.args:
        result = trip_controller.lists()
    else:
        if request.args.get('date'):
            date = request.args.get('date')
            result = trip_controller.filter_by_date(date)
        if request.args.get('region'):
            region = request.args.get('region')
            result = trip_controller.filter_by_region(region)
    if len(result) == 0:
        return jsonify({'message': 'No trips found.'}), 404
    trips = [trip._asdict() for trip in result]
    return jsonify({'trips': trips, 'trips_count': len(trips)}), 200


@app.route('/average_trips', methods=['GET'])
def get_average_trips():
    region = request.args.get('region')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date or not end_date or not region:
        return jsonify({'message': 'Region, start_date and end_date must be provided.'}), 400
    else:
        result = trip_controller.average_trips(region, start_date, end_date)
    if len(result) == 0:
        return jsonify({'message': 'No trips found.'}), 404
    trips = [trip for trip in result]
    return jsonify({'average_trips': trips, 'regions_count': len(trips)}), 200


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5005)), debug=True)
