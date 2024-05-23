import requests  # Used for making HTTP requests
import json  # Used for JSON manipulation
import logging  # Used for logging
from config import API_URL, API_KEY, GENERATION_CONFIG, SAFETY_SETTINGS  # Imports configuration settings

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

keys = [API_KEY, "AIzaSyBakZOIP9c4AqSbeGNfMQkoO07rRE_1Fw4"]
# keys=[API_KEY]
index = 0

def get_next_key():
    global index
    key = keys[index]
    index = (index + 1) % len(keys)
    return key

def generate_prompt_assessment(assessment_data):
    logging.info("Generating prompt for assessment.")
    logging.debug(f"Assessment data received: {assessment_data}")
    
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
        logging.error("Missing required assessment data.")
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
        logging.error("Missing required fields in one of the cards.")
        raise ValueError("Missing required fields in one of the cards")

    if int(no_of_questions) < 1:
        logging.error("Number of questions must be greater than 1.")
        raise ValueError("Number of questions must be greater than 1")

    if level.lower() not in ['low', 'medium', 'high']:
        logging.error("Level must be 'low', 'medium', or 'high'.")
        raise ValueError("Level must be 'low', 'medium', or 'high'")

    # Convert tools to comma-separated string
    tools_str = f" using {', '.join(tools)}" if tools else ""
    # Create the prompt
    prompt = f"I want {no_of_questions} assessment questions of {level} complexity for {role} on {', '.join(keywords)}{tools_str}."
    
    logging.info(f"Generated prompt: {prompt}")
    return prompt  # Return a list of formatted prompts

def get_result(prompt):
    logging.info("Generating result for prompt.")
    logging.debug(f"Prompt: {prompt}")
    
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
                    "High complexity should be Blooms level 4 of type analysis, preferably scenario-based. "
                    f"\n{prompt}")

    logging.debug(f"Final prompt: {final_prompt}")
    
    key = get_next_key()
    logging.info(f"Using key: {key}")

    try:
        # Set the API endpoint with authentication key
        apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"

        # Example format for multiple-choice questions to guide content generation
        example_format = (
            "MCQ strictly has to be in below format:\n"
            "Format:\n **Question 1 question**\n"
            "A. Option 1\n"
            "B. Option 2\n"
            "C. Option 3\n"
            "D. Option 4\n"
            "\n**Answer: Option no. Answer**\n"
            "MCQ Format Example:\n"
            "**Question 10**\n"
            "What is the purpose of the following code?\n"
            "```c\n"
            "int arr[] = {1, 2, 3, 4, 5};\n"
            "int sum, product;\n"
            "sum = product = 1;\n"
            "for (int i = 0; i < 5; i++) {\n"
            "  sum += arr[i];\n"
            "  product *= arr[i];\n"
            "}\n"
            "```\n"
            "A. To calculate the sum and product of all elements in the array\n"
            "B. To calculate the average and standard deviation of all elements in the array\n"
            "C. To reverse the order of elements in the array\n"
            "D. To sort the elements in the array\n"
            "\n**Answer: A. To calculate the sum and product of all elements in the array**\n"
            "No need to separate questions topic-wise and mention the topic and Write complete answer don't change the example format, all MCQ questions should be in given format"
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
        logging.info("Received response from API.")
        logging.debug(f"Generated content: {answer}")
        return answer  # Return the generated content

    except requests.exceptions.RequestException as e:
        logging.error("Service Exception:", exc_info=True)
        raise Exception("Error in getting response from Gemini API")
