import os
import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from controller import trip_controller
# , region_controller


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


# @app.route('/regions', methods=['GET'])
# def get_regions():
#     result = region_controller.lists()
#     if len(result) == 0:
#         return jsonify({'message': 'No regions found.'}), 404
#     regions = [region._asdict() for region in result]
#     return jsonify({'regions': regions, 'regions_count': len(regions)}), 200


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5005)), debug=True)
