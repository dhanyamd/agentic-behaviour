import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent import Agent 
from tools.tool import tool
agent1 = Agent(
    name="Poet Agent",
    backstory="You are a well known poet, who enjoys creating high quality poetry",
    task_description="Write a poem about meaning of friendship",
    task_expected_output="Just output the poem, without aby title or introductory sentences"
)
agent2 = Agent(
    name="Poem translator agent",
    backstory="You are an expert translator especially skilled in Ancient Roman",
    task_description="Translate a poem into Ancient Roman",
    task_expected_output="Just output the translated poem and nothing else"
)

agent1 >> agent2
print(agent1.dependencies) 
print(agent1.dependents)
print(agent2.dependencies),
print(agent2.dependents)

print(agent1.run())

print(agent2.context)
print(agent2.run())
