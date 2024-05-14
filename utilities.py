import requests  # Used for making HTTP requests
import json  # Used for JSON manipulation
from config import API_URL, API_KEY, GENERATION_CONFIG, SAFETY_SETTINGS  # Imports configuration settings

def generate_prompt_assessment(assessment_data):
    """
    Generates a list of assessment prompts based on provided assessment data.

    Parameters:
    assessment_data (dict): A dictionary containing the keys 'role', 'keywords', 'levels', and optionally 'toolsTechnologies'.
        Each 'level' should have 'noOfQuestion' and 'level' keys to specify the number of questions
        and the difficulty level respectively. 'toolsTechnologies' is a list of strings representing the tools and technologies used.

    Returns:
    list: A list of strings, where each string is a formatted prompt for generating questions, optionally including tools and technologies.

    Raises:
    ValueError: If the required keys are missing in `assessment_data` or any of its 'levels'.
    """
      
    # Check if the provided data has all required keys except toolsTechnologies which is optional
    required_keys = ['role', 'keywords', 'levels']
    if not all(key in assessment_data for key in required_keys):
        raise ValueError("Missing required assessment data")

    # Retrieve tools and technologies if provided
    tools_technologies = assessment_data.get('toolsTechnologies', [])
    tools_technologies_str = ", ".join(tools_technologies)  # Convert list to comma-separated string

    # Generate prompts based on the provided assessment data
    prompts = []
    for level_data in assessment_data['levels']:
        print(level_data)
        # if not all(key in level_data for key in ['level','noOfQuestions']):
            # raise ValueError("Missing level information in assessment data")
    
    # Check if the number of questions is greater than 1
        if int(level_data['noOfQuestions']) < 1:
            raise ValueError("Number of questions must be greater than 1")
        
     # Check if the level is valid (case insensitive)
        if level_data['level'].lower() not in ['easy', 'medium', 'complex']:
            raise ValueError("Level must be 'easy', 'medium', or 'complex'")

    # Append tools and technologies to the prompt if available
        tools_str = f" using {tools_technologies_str}" if tools_technologies else ""
        prompt = f"I want {level_data['noOfQuestions']} assessment questions of {level_data['level']} complexity for {assessment_data['role']} on {', '.join(assessment_data['keywords'])}{tools_str}."
        prompts.append(prompt)

    return prompts  # Return a list of formatted prompts


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
    final_prompt = "I am creating an assessment with the following specifications. Easy complexity should be blooms level 1 and 2 that test recall and comprehension. Medium complexity should be blooms level 3 of type application. Complex complexity should be blooms level 4 of type analytics, preferably scenario-based"
    final_prompt += f"\n {prompt}"  # Append the specific prompt details to the final prompt
    print(final_prompt)

    # Exception handling for HTTP requests
    try:
        # Set the API endpoint with authentication key
        apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
        

        # Example format for multiple-choice questions to guide content generation
        exampleFormat = "MCQ strictly has to be in below format:" + \
                        "Format: \n **Question 1 question" + \
                        "\nA. Option 1" + \
                        "\nB. Option 2" + \
                        "\nC. Option 3" + \
                        "\nD. Option 4" + \
                        "\n**Answer: A. Option 1 "+\
                        "\n no need to separate questions topic wise and mentioned the topic"

        # Request body containing content parts, generation configuration, and safety settings
        requestBody = {
            "contents": [{"parts": [{"text": final_prompt + exampleFormat}]}],
            "generationConfig": GENERATION_CONFIG,
            "safetySettings": SAFETY_SETTINGS
        }

        headers = {"Content-Type": "application/json"}  # HTTP headers for the request

        # Make a POST request to the API
        response = requests.post(apiUrl, data=json.dumps(requestBody), headers=headers)
        # Extract the generated content from the response
        answer = response.json().get("candidates")[0].get("content").get("parts")[0].get("text")
        print(answer)
        return answer  # Return the generated content

    except Exception as e:
        print(" Service Exception:", e)
        raise Exception("Error in getting response from Gemini api")
