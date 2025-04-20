import json 
import re 
import math
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from groq import Groq

from tools.tool import tool
from tools.tool import Tool, validate_arguments

from reflection.completions import build_prompt_structure
from reflection.completions import ChatHistory
from reflection.completions import completions_create
from reflection.completions import update_chat_history
from reflection.extractions import extract_tag_content

load_dotenv()

BASE_SYSTEM_PROMPT = ""


REACT_SYSTEM_PROMPT = """
You operate by running a loop with the following steps: Thought, Action, Observation.
You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don' make assumptions about what values to plug
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.

For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:

<tool_call>
{"name": <function-name>,"arguments": <args-dict>, "id": <monotonically-increasing-id>}
</tool_call>

Here are the available tools / actions:

<tools>
%s
</tools>

Example session:

<question>What's the current temperature in Madrid?</question>
<thought>I need to get the current weather in Madrid</thought>
<tool_call>{"name": "get_current_weather","arguments": {"location": "Madrid", "unit": "celsius"}, "id": 0}</tool_call>

You will be called again with this:

<observation>{0: {"temperature": 25, "unit": "celsius"}}</observation>

You then output:

<response>The current temperature in Madrid is 25 degrees Celsius</response>

Additional constraints:

- If the user asks you something unrelated to any of the tools above, answer freely enclosing your answer with <response></response> tags.
"""

class ReactAgent:
    """
    A class that represents an agent using the ReAct logic that interacts with tools to process
    user inputs, make decisions, and execute tool calls. The agent can run interactive sessions,
    collect tool signatures, and process multiple tool calls in a given round of interaction.

    Attributes:
        client (Groq): The Groq client used to handle model-based completions.
        model (str): The name of the model used for generating responses. Default is "llama-3.3-70b-versatile".
        tools (list[Tool]): A list of Tool instances available for execution.
        tools_dict (dict): A dictionary mapping tool names to their corresponding Tool instances.
    """

    def __init__(
        self,
        tools: Tool | list[Tool],
        model: str = "llama-3.3-70b-versatile",
        system_prompt: str = BASE_SYSTEM_PROMPT,
    ) -> None:
        self.client = Groq()
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools if isinstance(tools, list) else [tools]
        self.tools_dict = {tool.name: tool for tool in self.tools}

    def add_tool_signatures(self) -> str:
        """
        Collects the function signatures of all available tools.

        Returns:
            str: A concatenated string of all tool function signatures in JSON format.
        """
        return "".join([tool.fn_signature for tool in self.tools])

    def process_tool_calls(self, tool_calls_content: list) -> dict:
        """
        Processes each tool call, validates arguments, executes the tools, and collects results.

        Args:
            tool_calls_content (list): List of strings, each representing a tool call in JSON format.

        Returns:
            dict: A dictionary where the keys are tool call IDs and values are the results from the tools.
        """
        observations = {}
        for tool_call_str in tool_calls_content:
            tool_call = json.loads(tool_call_str)
            tool_name = tool_call["name"]
            tool = self.tools_dict[tool_name]

            print( f"\nUsing Tool: {tool_name}")

            # Validate and execute the tool call
            validated_tool_call = validate_arguments(
                tool_call, json.loads(tool.fn_signature)
            )
            print( f"\nTool call dict: \n{validated_tool_call}")

            result = tool.run(**validated_tool_call["arguments"])
            print(f"\nTool result: \n{result}")

            # Store the result using the tool call ID
            observations[validated_tool_call["id"]] = result
        return observations 

    def run(
        self,
        user_msg: str,
        max_rounds: int = 10,
    ) -> str: 
        """
        Executes a user interaction session, where the agent processes user input, generates responses,
        handles tool calls, and updates chat history until a final response is ready or the maximum
        number of rounds is reached.

        Args:
            user_msg (str): The user's input message to start the interaction.
            max_rounds (int, optional): Maximum number of interaction rounds the agent should perform. Default is 10.

        Returns:
            str: The final response generated by the agent after processing user input and any tool calls.
        """
        user_prompt =  build_prompt_structure(
              prompt=user_msg, role="user", tag="question"
        )
        if self.tools:
            self.system_prompt += (
                "\n" + REACT_SYSTEM_PROMPT % self.add_tool_signatures()
            )

        chat_history = ChatHistory(
            [
                build_prompt_structure(
                    prompt=self.system_prompt,
                    role="system",
                ),
                user_prompt,
            ]
        )

        if self.tools:
            # Run the ReAct loop for max_rounds
            for _ in range(max_rounds):
                
                completion = completions_create(self.client, chat_history, self.model)
                print("COMPLE",completion)
                response = extract_tag_content(str(completion), "response")
                print("RES",response)
                if response.found:
                    return response.content[0]

                thought = extract_tag_content(str(completion), "thought")
                tool_calls = extract_tag_content(str(completion), "tool_call")
                update_chat_history(chat_history, completion, "assistant")

                # Check if thought tag was found before printing
                if thought.found:
                    print( f"\nThought: {thought.content[0]}")
                else:
                    print("\nThought: (No thought tag found)")

                if tool_calls.found:
                    observations = self.process_tool_calls(tool_calls.content)
                    print(f"\nObservations: {observations}")
                    update_chat_history(chat_history, f"{observations}", "user")
               
        return completions_create(self.client, chat_history, self.model)
   
@tool
def sum_two_elements(a: int, b:int) -> int : 
     """
     computes the sum 
     """
     return a + b 
@tool 
def multiply_two_elements(a: int, b:int) -> int :
     """multiply"""
     return a * b 
@tool 
def compute_log(x:int) -> float | str: 
     if x <= 0:
          return "Logarithm is undefined for values less than or equal to 0"
     return math.log(x)
available_tools = {
     "sum_two_elements": sum_two_elements,
     "multiply_two_elements": multiply_two_elements,
     "compute_log" : compute_log
}

agent = ReactAgent(tools=[sum_two_elements, multiply_two_elements, compute_log])
agent.run(user_msg="I want to calculate the sum of 1234 and 5678 and multiply the result by 5. Then i want to find the logarithm of that result")
