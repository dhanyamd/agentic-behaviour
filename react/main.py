import json 
import re 
import math
import sys
import os

from react import ReactAgent

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from groq import Groq

from tools.tool import tool
from tools.tool import Tool, validate_arguments
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
