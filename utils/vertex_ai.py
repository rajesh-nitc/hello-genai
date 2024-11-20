import logging
import os

from vertexai.generative_models import (
    GenerationConfig,
    GenerationResponse,
    GenerativeModel,
)

from tools.spend import spend_tool

logger = logging.getLogger(__name__)


def extract_function_call(response: GenerationResponse) -> dict:
    """
    Extracts a single function call from the model's response.

    Args:
        response (GenerationResponse): The model's response.

    Returns:
        dict: A dictionary representing the function call and its arguments.
    """
    if response.candidates and response.candidates[0].function_calls:
        function_call = response.candidates[0].function_calls[0]
        function_call_dict = {function_call.name: dict(function_call.args)}
        logger.info(f"function_call_dict: {function_call_dict}")

        return function_call_dict

    logger.info("No function call found in the model response.")
    return {}


def extract_text(response: GenerationResponse, user_id: str) -> str:
    """
    Extracts text content from the response and appends it to the history for the user.

    Args:
        response (GenerationResponse): The model's response.
        user_id (str): The unique identifier for the user.

    Returns:
        str: The extracted text.
    """
    # Extract text from the model's response
    text = response.candidates[0].content.parts[0].text
    logger.info(f"Extracted text: {text}")

    return text


def get_model() -> GenerativeModel:
    """
    Returns a configured GenerativeModel object.

    Raises:
        ValueError: If the MODEL_NAME environment variable is not set.

    Returns:
        GenerativeModel: A configured generative model instance.
    """
    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("MODEL_NAME environment variable is not set.")

    logger.info(f"Initializing GenerativeModel with model_name: {model_name}")

    return GenerativeModel(
        model_name,
        generation_config=GenerationConfig(temperature=0, candidate_count=1),
        tools=[spend_tool],
    )