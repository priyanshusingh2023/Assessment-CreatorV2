from flask_restx import Resource, Namespace, fields, reqparse
from services import generate_assessment  # Import the generate_assessment function from services module

api = Namespace('Assessment_creator', description='Main operations for creating assessments')

# Model for level structure in the request body
level_model = api.model('levels', {
    'level': fields.String(required=True, description='Difficulty level of the questions'),
    'noOfQuestions': fields.Integer(required=True, description='Number of questions for the level')

})

# Model for the entire assessment request body
assessment_request_model = api.model('AssessmentRequest', {
    'role': fields.String(required=True, description='Role of the person for whom questions are created'),
    'keywords': fields.List(fields.String, required=True, description='Keywords associated with the questions'),
    'toolsTechnologies': fields.List(fields.String, required=True, description='Tools and technologies involved in the questions'),
    'levels': fields.List(fields.Nested(level_model), required=True, description='List of levels with question count and difficulty')
})

@api.route('/')
class Hello(Resource):
    def get(self):
        """
        A simple endpoint to return a greeting. Useful for verifying that the API is operational.

        Returns:
        str: A greeting message indicating the API is up and running.
        """
        return "Hello From Assessment Creator Back-End"

@api.route('/generate_assessment')
class GenerateAssessment(Resource):
    @api.expect(assessment_request_model)
    def post(self):
        """
        Receives assessment configuration data as JSON, validates it, and uses it to generate an assessment.

        Processes the incoming JSON data, validates presence of all required fields, and calls the assessment
        generation service. Handles various errors and exceptions by returning appropriate HTTP status codes and
        error messages.

        Returns:
        dict, int: A dictionary containing the generated assessment text on success or an error message on failure,
                   accompanied by the appropriate HTTP status code.
        """
        try:
            assessment_data = api.payload  # Extract JSON data from the request payload
            if not assessment_data:
                return {"error": "No data provided or invalid JSON format"}, 400

            response = generate_assessment(assessment_data)
            return {"assessment": response}, 200

        except KeyError as e:
            return {"error": f"Missing key in input data: {str(e)}"}, 400

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

def configure_routes(api_instance):
    """
    Configures routes for the Flask application by adding the defined Namespace to the Flask instance.

    Parameters:
    api_instance (Flask): The Flask application or API instance where the Namespace is to be added.

    This function ensures that all defined routes and resources under the 'Assessment_creator' Namespace
    are registered with the Flask application, enabling their accessibility via HTTP requests.
    """
    api_instance.add_namespace(api)
