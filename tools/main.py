import json 
import requests 
from tool import tool 
from tool_pattern import ToolAgent 

def fetch_top_hacker_news_stories(top_n: int): 
    """ 
    Fetch the top stories from hacker news.

    This function retrieves the top_n stories from hacker news api. 
    Each story contains title, url, score, author and tos. The data fetched 
    is returned in json format.

    Args: 
    top_n(int) : The number of top stories to retrieve.

    """
    top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    try:
       response = requests.get(top_stories_url)
       response.raise_for_status()
       top_story_ids = response.json()[:top_n]
       top_stories = [] 

       for story_id in top_story_ids:
           story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
           story_response = requests.get(story_url)
           story_response.raise_for_status()
           story_data = story_response.json()

           top_stories.append({
               'title': story_data.get('title', 'No title'),
               'url': story_data.get('url', 'No url avaialable')
           })
       return json.dumps(top_stories)

    except requests.exceptions.RequestException as e: 
        print("An error occured")
        return []

json.loads(fetch_top_hacker_news_stories(top_n=5))

hn_tool = tool(fetch_top_hacker_news_stories)
hn_tool.name 
print("TOOOL FN",hn_tool.fn)
print("TOOOL FN SIGN",hn_tool.fn_signature)

tool_agent = ToolAgent(tools=[hn_tool])
output = tool_agent.run(user_msg="Tell me the top 5 Hacker News stories right now") 
print(output)