from crew import Crew
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent import Agent 
from run import write_str_to_txt
with Crew() as crew : 
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

 agent3 = Agent(
     name="Writer Agent",
    backstory="You are an expert transcriber, that loves writing poems into txt files",
    task_description="You'll recieve a Roaman poem in your context. You need to write the poem into './poem.txt' file",
    task_expected_output="A .txt file containing the roman poem recieved from the context",
    tools=write_str_to_txt
)
 agent1 >> agent2 >> agent3 

(crew.plot())
(crew.run())
print("hii")
print(crew.plot())
