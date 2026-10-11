import os 
import argparse
import sys
import json
from prompts import system_prompt
from openai import OpenAI
from dotenv import load_dotenv
from call_function import available_functions, call_function
from generate_content import generate_content

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("invalid api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(10):
    result = generate_content(client, messages, args)
    if result is not None:
        print(result)
        break
else:
    print(f"Error: Failed to produce a response")
    sys.exit(1)