from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='ezwq2173',
            host='localhost',
            port='5432'  # Default port for PostgreSQL
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    barcode = data.get('barcode')

    if barcode:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed!'}), 500
        
        try:
            cursor = conn.cursor()
            # Check if barcode already exists
            cursor.execute('SELECT COUNT(*) FROM barcode WHERE barcode_value = %s', (barcode,))
            count = cursor.fetchone()[0]

            if count > 0:
                return jsonify({'message': 'Barcode already exists!'}), 409  # Conflict

            # Insert barcode and current timestamp into the database
            cursor.execute('INSERT INTO barcode (barcode_value, created_at) VALUES (%s, %s)', (barcode, datetime.now()))
            conn.commit()
            cursor.close()
            return jsonify({'message': 'Barcode stored successfully!'}), 201
        except Exception as e:
            print(f"Error storing barcode: {e}")
            return jsonify({'error': 'Failed to store barcode'}), 500
        finally:
            conn.close()
    return jsonify({'error': 'No barcode provided!'}), 400


if __name__ == '__main__':
    app.run(port=5000)
