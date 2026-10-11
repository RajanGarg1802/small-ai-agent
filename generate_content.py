import os 
import argparse
import json
from prompts import system_prompt
from openai import OpenAI
from dotenv import load_dotenv
from call_function import available_functions, call_function

def generate_content(client, messages, args):
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages = messages,
        tools = available_functions,
        temperature = 0,
    )
    if response.usage is None:
        raise RuntimeError("API Request Failed")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    
    our_message = response.choices[0].message
    messages.append(our_message)
    if our_message.tool_calls:
        for tool_call in our_message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            result_message = call_function(tool_call, args.verbose)
            if not result_message["content"]:
                raise Exception()
            messages.append(result_message)
            if args.verbose:
                print (f'-> {result_message["content"]}')

    else:
        return our_message.content