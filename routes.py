from flask_restx import Resource, Namespace, fields, reqparse
from services import generate_assessment  # Import the generate_assessment function from services module
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api = Namespace('Assessment_creator', description='Main operations for creating assessments')

# Model for card structure in the request body
card_model = api.model('Card', {
    'keywords': fields.List(fields.String, required=True, description='Keywords associated with the questions'),
    'tools': fields.List(fields.String, required=True, description='Tools and technologies involved in the questions'),
    'level': fields.String(required=True, description='Difficulty level of the questions'),
    'noOfQuestions': fields.Integer(required=True, description='Number of questions for the level')
})

# Model for the entire assessment request body
assessment_request_model = api.model('AssessmentRequest', {
    'role': fields.String(required=True, description='Role of the person for whom questions are created'),
    'cards': fields.List(fields.Nested(card_model), required=True, description='List of cards with keywords, tools, level, and question count')
})

@api.route('/')
class Hello(Resource):
    def get(self):
        """
        A simple endpoint to return a greeting. Useful for verifying that the API is operational.

        Returns:
        str: A greeting message indicating the API is up and running.
        """
        logging.info("Hello endpoint called.")
        return "Hello From Assessment Creator Back-End"

@api.route('/generate_assessment')
class GenerateAssessment(Resource):
    
    @api.expect(assessment_request_model)
    def post(self):
        logging.info("GenerateAssessment endpoint called.")
        try:
            assessment_data = api.payload  # Extract JSON data from the request payload
            logging.debug(f"Received assessment data: {assessment_data}")

            if not assessment_data:
                logging.warning("No data provided or invalid JSON format.")
                return {"error": "No data provided or invalid JSON format"}, 400

            response = generate_assessment(assessment_data)
            logging.info("Assessment generated successfully.")
            return {"assessment": response}, 200

        except KeyError as e:
            logging.error(f"Missing key in input data: {str(e)}")
            return {"error": f"Missing key in input data: {str(e)}"}, 400

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            return {"error": f"An error occurred: {str(e)}"}, 500

def configure_routes(api_instance):
    """
    Configures routes for the Flask application by adding the defined Namespace to the Flask instance.

    Parameters:
    api_instance (Flask): The Flask application or API instance where the Namespace is to be added.

    This function ensures that all defined routes and resources under the 'Assessment_creator' Namespace
    are registered with the Flask application, enabling their accessibility via HTTP requests.
    """
    logging.info("Configuring routes for the API.")
    api_instance.add_namespace(api)
