import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Get Pushover credentials from environment variables
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

# Define the Pushover API endpoint
pushover_url = "https://api.pushover.net/1/messages.json"

# Send an owner notification through Pushover; model-facing functions below
# reuse this transport so notification details stay in one place.
# Define a function to send a message to Pushover
def push(text):
    requests.post(
        pushover_url,
        data={
            "token": pushover_token,
            "user": pushover_user,
            "message": text,
        },
    )

# Convert a visitor's voluntary contact request into an owner notification.
#  Define the tools that can be called by the agent
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"

# Notify the owner about a knowledge gap instead of allowing the twin to guess.
# Define the tools that can be called by the agent
def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"

# Define the tools that can be called by the agent
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

# Define the tools that can be called by the agent
record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

# Define the tools that can be called by the agent
# Publish only these JSON schemas to the model; Python functions themselves are
# never passed to the provider.
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

# Define a mapping of tool names to their corresponding functions
# Explicit dispatch prevents an arbitrary model-supplied function name from
# resolving through Python globals.
tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


# Execute a batch of model tool requests and return Chat Completions-compatible
# tool messages that let the model finish its response.
# The legacy comment below mentions globals, but this implementation deliberately
# dispatches through the explicit tool_map allowlist above.
# This function can take a list of tool calls, and run them. This is the globals() version!!
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
