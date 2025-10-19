from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_sum(number1,number2):
    print("Tool called with:", number1,number2)
    result = number1+number2
    return {"result": result}

def get_multiply(number1,number2):
    print("Tool called with:", number1, number2)
    return {"result": number1*number2}

def get_pow(number1, number2):
    print("Tool called with:", number1, number2)
    return {"result": number1**number2}



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_sum",
            "description": "return the sum of numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "number1": {"type": "number", "description": "sum of number"},
                    "number2": {"type": "number", "description": "sum of number"},
                },
               "required": ["number1","number2"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_multiply",
            "description": "return the multiplication of number",
            "parameters": {
                "type": "object",
                "properties": {
                    "number1": {"type": "number","description": "number to multiply"},
                    "number2": {"type": "number","description": "multiply number"},
                },
               "required": ["number1","number2"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pow",
            "description": "return the power of number",
            "parameters": {
                "type": "object",
                "properties": {
                    "number1": {"type": "number","description": "number to power"},
                    "number2": {"type": "number","description": "power of number"},
                },
               "required": ["number1","number2"]
            },
        },
    }
]


SYSTEM_PROMPT = """
    You are an expert ai assistant in resolving user queries using chain of thought.
    You work on START,PLAN,OUTPUT steps.
    You need first PLAN and what needs to be done. The plan can be multiple steps.
    once you think enough PLAN has been done, finally give an OUTPUT.

    Rules: 
        - strictly follow the give json output format
        - only run one step at time
        - The sequence of steps is START(where user gives an inputs), PLAN(that can be multiple times), OUTPUT(which
        is going display to user)
    
        OUTPUT JSON Format:
            {"step": "START" |"PlAN" | "OUTPUT", "content":"string" }

        Example: 
        "START": Hey, can you solve 2+3*5/10"
        "PLAN": {"step":"PLAN", content:"seems like user is intrested in maths problem"}
        "PLAN": {"step":"PLAN", content:"looking at problem, we should solve using BODMAS method"}
        "PLAN": {"step":"PLAN", content:"Yes, The BODMAS is the correct thing to be done here"}
        "PLAN": {"step":"PLAN", content:"First we must multiply 3*5 which is 15"}
        "PLAN": {"step":"PLAN", content:"First we must multiply 3*5 which is 15"}
        "PLAN": {"step":"PLAN", content:"Now the equation is 2+15"}
        "PLAN": {"step":"PLAN", content:"Now we must perform that is 15/10 = 1.5"}
        "PLAN": {"step":"PLAN", content:"Now the equation is 2+1.5"}
        "PLAN": {"step":"PLAN", content:"Finally now perform that add 3.5"}
        "OUTPUT": {"step":"OUTPUT", content:"Great we have solved and finally left with 3.5 answer"}
"""

history = [
            {"role": "system", "content": "You are a helpful assistant in doing arithmetic opearations"},
            {"role": "user", "content": "First calculate 3+4 then multiply by 2 then raise it to the power of 2 ?"}
           ]

tool_map = {
    "get_sum": get_sum,
    "get_multiply": get_multiply,
    "get_pow": get_pow,
}
while True:
    print("--------------------")
    print("Sending request to model with history:")
    completion = client.chat.completions.create(
        model="gemini-flash-latest",
        messages=history,
        tools=tools
    )
    
    response_message = completion.choices[0].message
    # Check if the model wants to call tools
    if response_message.tool_calls:
        # Add the assistant's response (with tool calls) to history
        print(response_message)
        history.append(response_message)
        
        # Execute each tool call
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            
            if function_name in tool_map:
                function_to_call = tool_map[function_name]
                function_args = json.loads(tool_call.function.arguments)
                
                # Call the actual Python function
                function_response = function_to_call(**function_args)
                
                # Add the tool's output to history
                history.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    }
                )
            else:
                print(f"Error: Model tried to call unknown function '{function_name}'")

        # Continue the loop to let the model process the tool results
        continue 
    else:
        # If no tool calls, the model has given its final answer.
        print(response_message)
        final_answer = response_message.content
        print("\n===== FINAL ANSWER =====")
        print(final_answer)
        break # Exit the loop