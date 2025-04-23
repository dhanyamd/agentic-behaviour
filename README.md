   **THIS IS A REPOSITORY MADE FOR STUDYING FOUR DIFFERENT AGENTIC BEHAVIOURS AND PATTERNS THROUGH HANDS ON IMPLEMENTATION**
 *****

1) **Reflection pattern :**
   
   The Agent takes the prompt and generates a output using Groq as the LLM Model, it then starts a loop and passes it down to reflection function which iterates and finds inconcsistencies in the answer
   and re-generates it's answer. The reflection agent comes up with a much more concise answer with suitable reasoning. This is a iterative process within a loop set to a certain number, in our case 3
   which means the whole thinking and reflective process runs for three steps to provide the best optimal result at the end.
  
   
3) **Tool Calling Agent :**

    This is a custom agent class made with python which converts any function into a tool calling agent which can be invoked using the @tool decorator. The Tool class takes a name, fn and function
    signature and generates a function signature with the name, arguments and descriptions for each. The LLM identifies what tool to call given multiple tools defined and call the necessary function
    which in our case is the fetch_hacker_news_fn which fetches the top 5 news with title and url
   

5) **ReAct pattern :**
   
    This agent works on iterating through thought, action, observation untils it reaches a final response. It is what's a Planning Pattern provides; ways for the LLM to break a task into smaller, more easily
    accomplished subgoals without losing track of the end goal. Here in this implementation it runs through a loop and is provided with multiple tools, it selects which tools specifically to use under which
    operation and generates <thought> and the tool call dict for each process in the loop subsequently and keeps on looping until it reaches the final response. This is just a mini implementation of ReAct
    agent under the hood


7) **Multi-agent pattern :**
   
    This agent is an example implementation of crews and multiple agents working together providing one's output as context to another agent to execute multiple calls simultaneously. This illustrates how
    multiple agents with different functions can exist together and how one's response is crucial to be fed into as context to the other. We here use two agents poem agent and poem translater agent where
    the latter depends on the former. We define their dependencies and register them in a crew which orders them in a toplogical sort (perform DAG) and lets u visually plot them. This agent also uses ReAct
    architecture under the hood.
   

   *****
