import sys
import os

# Add the parent directory (agents) to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent import Agent 
from tools import tool

agent_example = Agent(
    name="Poet Agent",
    backstory="You are a well known poet, who enjoys creating high quality poetry",
    task_description="Write a poem about meaning of friendship",
    task_expected_output="Just output the poem, without aby title or introductory sentences"
)

print(agent_example.run())

