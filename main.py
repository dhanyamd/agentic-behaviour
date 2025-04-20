from reflection import ReflectionAgent 

agent = ReflectionAgent()

generation_system_prompt = """ 

You are a python programmer tasked with high wuality python code. 
Your task is to generate the best content possible for the user's request. If the user provides 
critique, respond with a revised version of your previosu attempt
"""
reflection_system_prompt = """ 
You are Andrej Karpathy, an experienced computer engineer. You are tasked with generating 
critique and recommendations for the user's code.
"""

prompt = """ 
Generate a Python implementation of the Merge Sort algorithm
"""
final_response = agent.run(
    generation_system_prompt=generation_system_prompt,
    reflection_system_prompt=reflection_system_prompt,
    user_msg=prompt,
    n_steps=3,
    verbose=1
)