from flask import Flask  # Import the Flask class to create a Flask application
from flask_cors import CORS  # Import CORS to enable Cross-Origin Resource Sharing
from flask_restx import Api  # Import Api from Flask-RESTx to structure the RESTful API
from routes import configure_routes  # Import function to configure API routes

app = Flask(__name__)  # Create a Flask application instance
CORS(app)  # Apply CORS to the Flask app to allow cross-origin requests

# Configure the API with a base prefix, version, title, and description
api = Api(app, prefix='/api/v2', version='1.0', title='Assessment Creator', description='Assessment Creator Back-end')

configure_routes(api)  # Add the configured routes to the API

if __name__ == '__main__':
    # The following block is executed if the script is run directly (i.e., not imported as a module).
    app.run(debug=True)  # Start the Flask application with debugging enabled
