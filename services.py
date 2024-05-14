from utilities import get_result, generate_prompt_assessment  # Imports necessary functions from utilities module

def generate_assessment(assessment_data):
    """
    Generates an assessment based on provided data by creating specific prompts and using an API to generate content.

    This function orchestrates the generation of assessment questions by first formatting prompts based on input
    data about the assessment, and then using these prompts to generate actual assessment content via an external API.

    Parameters:
    assessment_data (dict): A dictionary containing all necessary data to generate assessment prompts. The structure
        and required keys are dictated by the `generate_prompt_assessment` function.

    Returns:
    str: A string containing all the generated assessment questions, concatenated together.

    Raises:
    ValueError: If `assessment_data` is not a dictionary or is empty, indicating invalid or insufficient input data.
    """
    # Validate input data
    if not isinstance(assessment_data, dict) or not assessment_data:
        raise ValueError("Invalid assessment data provided")

    result = ""  # Initialize a variable to store all generated content
    # Generate prompts from the assessment data
    prompts_entry = generate_prompt_assessment(assessment_data)
    for prompt in prompts_entry:
        # Generate assessment content for each prompt using an external API
        res = get_result(prompt)
        result += res + "\n\n"  # Concatenate the results into a single string
    return result  # Return the final concatenated result
