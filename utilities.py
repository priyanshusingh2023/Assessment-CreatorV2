import requests  # Used for making HTTP requests
import json  # Used for JSON manipulation
from config import API_URL, API_KEY, GENERATION_CONFIG, SAFETY_SETTINGS  # Imports configuration settings

def generate_prompt_assessment(assessment_data):
    print(assessment_data)
    """
    Generates a list of assessment prompts based on provided assessment data.

    Parameters:
    assessment_data (dict): A dictionary containing the keys 'role' and 'cards'.
        Each 'card' should have 'keywords', 'tools', 'level', and 'noOfQuestions'.

    Returns:
    list: A list of strings, where each string is a formatted prompt for generating questions, optionally including tools and technologies.

    Raises:
    ValueError: If the required keys are missing in `assessment_data` or any of its 'cards'.
    """
    # Check if the provided data has all required keys
    required_keys = ['role', 'card']
    if not all(key in assessment_data for key in required_keys):
        raise ValueError("Missing required assessment data")

    role = assessment_data['role']
    card = assessment_data['card']




    # Generate prompts based on the provided assessment data
    prompts = []
    keywords = card.get('keywords')
    tools = card.get('tools', [])
    level = card.get('level')
    no_of_questions = card.get('noOfQuestions')



        # Validate card fields
    if not (keywords and tools is not None and level and no_of_questions):
        raise ValueError("Missing required fields in one of the cards")

    if int(no_of_questions) < 1:
        raise ValueError("Number of questions must be greater than 1")

    if level.lower() not in ['low', 'medium', 'high']:
        raise ValueError("Level must be 'low', 'medium', or 'high'")

        # Convert tools to comma-separated string
    tools_str = f" using {', '.join(tools)}" if tools else ""
        # Create the prompt
    prompt = f"I want {no_of_questions} assessment questions of {level} complexity for {role} on {', '.join(keywords)}{tools_str}."

    print(prompt)
    return prompt  # Return a list of formatted prompts

def get_result(prompt):
    """
    Generates assessment questions based on a given prompt using an external API.

    Parameters:
    prompt (str): A string prompt that describes the type of questions to be generated.

    Returns:
    str: The generated content as a string containing the assessment questions.

    Raises:
    Exception: If there is any error in making the API request or processing the response.
    """
    # Predefined prompt for setting the context of generated content
    final_prompt = ("I am creating an assessment with the following specifications. "
                    "Low complexity should be Blooms level 1 and 2 that test recall and comprehension. "
                    "Medium complexity should be Blooms level 3 of type application. "
                    "Hight complexity should be Blooms level 4 of type analysis, preferably scenario-based. "
                    f"\n{prompt}")

    print(final_prompt)  # For debugging purposes

    try:
        # Set the API endpoint with authentication key
        apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

        # Example format for multiple-choice questions to guide content generation
        example_format = (
            "MCQ strictly has to be in below format:\n"
            "Format:\n **Question 1 question"+"\n"
            "A. Option 1"+"\n"
            "B. Option 2"+"\n"
            "C. Option 3"+"\n"
            "D. Option 4"+"\n"
            "\n**Answer: A. Option 1\n"
            "No need to separate questions topic-wise and mention the topic."
        )

        # Request body containing content parts, generation configuration, and safety settings
        request_body = {
            "contents": [{"parts": [{"text": final_prompt + example_format}]}],
            "generationConfig": GENERATION_CONFIG,
            "safetySettings": SAFETY_SETTINGS
        }

        headers = {"Content-Type": "application/json"}  # HTTP headers for the request

        # Make a POST request to the API
        response = requests.post(apiUrl, data=json.dumps(request_body), headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Extract the generated content from the response
        answer = response.json().get("candidates")[0].get("content").get("parts")[0].get("text")
        print(answer)  # For debugging purposes
        return answer  # Return the generated content

    except requests.exceptions.RequestException as e:
        print("Service Exception:", e)
        raise Exception("Error in getting response from Gemini API")
