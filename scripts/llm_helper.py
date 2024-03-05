import requests
url= "https://www.blackbox.ai/api/chat"
import json
from keys import OPEN_ROUTER_API_KEY as OPENROUTER_API_KEY
# {
#   "internal_alt_text": "a pink lego batman with the words i'm literally batman",
#   "followers": "116 followers",
#   "comments": "51 Comments",
#   "pinterest": "https://pinterest.com/pin/13581236381990031/",
#   "image_source": "https://i.pinimg.com/236x/b7/96/a8/b796a8fa52867ca9c92b397be909c142.jpg",
#   "image_outer_alt_text": "credits to @seorixoxo for the ideea<33 #whisper #whispergirlie #girlie #pinterest #pinterestgirlie #girlie #batman #pinkbatman #pink #batman #pinkbatman #follow4follow #like4like #save4save",
#   "blip_alt_text": "a close up of a pink lego batman with a bat"
# }

def generate_response(main_query, results: list):
    input_data= ""
    for data in results:
        relevant_data= f"""
        caption1:{data["internal_alt_text"]}
        caption2:{data["blip_alt_text"]}
        comments:{data["comments"]}
        followers:{data["followers"]}
        
        """
        
        input_data+=relevant_data
        
    prompt= f"""Generate a list of captions from following data containing captions of high ranking images around the keyword: {main_query}:
    
    ### Constraints: 
    1. The caption should be around the main keyword: {main_query}
    2. Give more importance to captions with less comments and less followers as they are more closer to the actual image description.
    
    Here is the data:
    {input_data}    
    """
    
    # response= requests.post(url, json={"messages":[{"id":"OfS3kB7","content":prompt,"role":"user"}],"id":"OfS3k7","previewToken":None,"userId":"0cf5b2a2-04cd-4107-b3d1-935498418149","codeModelMode":True,"agentMode":{},"trendingAgentMode":{},"isMicMode":False,"userSystemPrompt":None,"maxTokens":None,"webSearchMode":True,"promptUrls":None,"isChromeExt":False,"githubToken":None})
    
    response_gpt3 = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                },
                data=json.dumps({
                    "model": "openai/gpt-3.5-turbo", # Optional
                    "messages": [
                    {"role": "user", "content": prompt}
                    ]
                })
            )
        
    print("""
          [Generated LLM RESPONSE]
          """)
    return response_gpt3.json()
    
    
    
    
    