import os
import logging
# from import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin_lat = db.Column(db.Float, nullable=False)
    origin_long = db.Column(db.Float, nullable=False)
    dest_lat = db.Column(db.Float, nullable=False)
    dest_long = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)


@app.route('/trips', methods=['POST'])
def create_trip():
    data = request.get_json()
    trip = Trip(
        origin_lat=data['origin_lat'],
        origin_long=data['origin_long'],
        dest_lat=data['dest_lat'],
        dest_long=data['dest_long'],
        date=data['date'],
        time=data['time'],
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify({'message': 'Trip created successfully.'}), 201


@app.route('/average_trips', methods=['GET'])
def get_average_trips():
    data = request.get_json()
    bounding_box = data.get('bounding_box')
    region = data.get('region')
    start_date = data['start_date']
    end_date = data['end_date']

    if not (bounding_box or region):
        return jsonify({'message': 'Either bounding_box or region must be provided.'}), 400

    if bounding_box:
        query = (
            f"SELECT COUNT(*) / 7 AS average_trips FROM trip "
            f"WHERE origin_lat BETWEEN {bounding_box[0]} AND {bounding_box[2]} "
            f"AND origin_long BETWEEN {bounding_box[1]} AND {bounding_box[3]} "
            f"AND date BETWEEN '{start_date}' AND '{end_date}'"
        )
    else:
        query = (
            f"SELECT COUNT(*) / 7 AS average_trips FROM trip "
            f"WHERE ST_Intersects(ST_GeomFromText('{region}'), "
            f"ST_Point(origin_lat, origin_long)) "
            f"AND date BETWEEN '{start_date}' AND '{end_date}'"
        )

    result = db.engine.execute(query).fetchone()

    if result is None:
        return jsonify({'message': 'No trips found.'}), 404

    return jsonify({'average_trips': result[0]}), 200


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
