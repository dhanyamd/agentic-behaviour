import sys
import os

# Add the parent directory (agents) to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent import Agent 
from tools.tool import tool

agent_example = Agent(
    name="Poet Agent",
    backstory="You are a well known poet, who enjoys creating high quality poetry",
    task_description="Write a poem about meaning of friendship",
    task_expected_output="Just output the poem, without aby title or introductory sentences"
)

print(agent_example.run())


@tool 
def write_str_to_txt(string_data: str, txt_filename: str) :
    with open(txt_filename, mode='w', encoding='utf') as file: 
        file.write(string_data) 

    print(f"Data successfully written to {txt_filename}")

agent_tool_example = Agent(
     name="Writer Agent",
    backstory="You are a language model specialised in writing text into .txt files",
    task_description="Write the string 'This is a Tool Agent' into ./tool_agent_example.txt",
    task_expected_output="A .txt file containing the given string",
    tools=write_str_to_txt
)
agent_tool_example.run()
