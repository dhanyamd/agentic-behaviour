**THIS IS A REPOSITORY MADE TO STUDY DIFFERENT AGENTIC BEHAVIOURS AND PATTERNS BY REAL HANDS ON IMPLEMENTATION**

1) **Reflection pattern**
   The Agent takes the prompt and generates a output using Groq as the LLM Model, it then starts a loop and passes it down to reflection function which iterates and finds inconcsistencies in the answer
   and re-generates it's answer. The reflection agent comes up with a much more concise answer with suitable reasoning. This is a iterative process within a loop set to a certain number, in our case 3
   which means the whole thinking and reflective process runs for three steps to provide the best optimal result at the end.
   
