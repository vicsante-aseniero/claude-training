"""
Main module for the Claude training examples.

Demonstrates how to initialize the Anthropic client and generate a response
using the Claude API.
"""

from typing import List

from anthropic import Anthropic
from anthropic.types import MessageParam
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic()
MODEL = "claude-sonnet-4-5"


def generate_response(messages: List[MessageParam]) -> str:
    """
    Generate a response from the Anthropic API based on the provided messages.

    Args:
        messages (List[MessageParam]): A list of message
            parameters for the conversation.

    Returns:
        str: The generated response from the model.
    """
    message = client.messages.create(
        model=MODEL, max_tokens=1024, messages=messages
    )
    return message.content[0].text


def str_replace_editor_tool():
    """
    Demonstrates sending a basic prompt to the Anthropic API.
    """

    messages = [
        {
            "role": "user",
            "content": (
                "Hi, I'm a human. Explain back to me in simple terms what's "
                "the difference between HTML and CSS."
            ),
        }
    ]

    response = generate_response(messages)
    print(response)


def code_generation_example():
    """
    Demonstrates asking the model to write some code.
    """

    messages = [
        {
            "role": "user",
            "content": (
                "Please write a simple Python function to compute the "
                "nth Fibonacci number."
            ),
        }
    ]

    response = generate_response(messages)
    print("\n--- Code Generation Example ---")
    print(response)


if __name__ == "__main__":
    print("--- Basic Prompt Example ---")
    str_replace_editor_tool()
    code_generation_example()
