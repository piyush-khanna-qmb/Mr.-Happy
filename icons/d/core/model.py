""" Importing all the neccessary libraries. """

import cohere 
from rich import print
from dotenv import dotenv_values
""" Setting the variables, which will be used in the automation. """

env_vars = dotenv_values("CONST")
CohereAPIKey = env_vars.get("CohereAPIKey")
co = cohere.Client(api_key= CohereAPIKey)
funcs = ["general","realtime","open","close","play","generate image","system","content","google search","youtube search","reminder"]

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is ( noun from history )', if the query is 'what's his networth?' respond with 'general what's ( noun from history ) networth?', if the query is 'tell me more about him.' respond with 'general tell me more about ( noun from history ).', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
-> Respond with 'open webcam' if a query is asking to open webcam.
-> Respond with 'close webcam' if a query is asking to close webcam.
*** if the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
*** If the user is saying 'exroza', esrora', 'axrora' or something rhyming like this, replace it to 'axzora'. ***
"""

FixedHistory = [
      {"role": "User", "message": "who was iron man"},
      {"role": "Chatbot", "message": "general who was iron man?"},
      {"role": "User", "message": "who is he"},
      {"role": "Chatbot", "message": "general who is iron man?"},]

ChatHistory = [
      {"role": "User", "message": "how are you?"}, 
      {"role": "Chatbot", "message": "general how are you?"}, 
      {"role": "User", "message": "do you like pizza?"}, 
      {"role": "Chatbot", "message": "general do you like pizza?"}, 
      {"role": "User", "message": "open chrome and tell me about mahatma gandhi."}, 
      {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."}, 
      {"role": "User", "message": "open chrome and firefox"}, 
      {"role": "Chatbot", "message": "open chrome, open firefox"}, 
      {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"}, 
      {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
      {"role": "User", "message": "chat with me."}, 
      {"role": "Chatbot", "message": "general chat with me."}]

def FirstLayerDMM(prompt:str="test", ChatHistory:list=ChatHistory) -> list[str]:
    stream = co.chat_stream( 
    model='command-r-plus',
    message=prompt,
    temperature=0.7,
    chat_history=FixedHistory+ChatHistory[-12:],
    prompt_truncation='OFF',
    connectors=[],
    preamble=preamble) 
    
    response = ""
    for event in stream:
        if event.event_type == "text-generation":
                response += event.text
    response2 = f"{response}"
    response = response.replace("\n", "")
    response = response.split(",")
    response = [i.strip() for i in response]
    temp = []
    for task in response:
        for func in funcs:
                if task.startswith(func):
                    temp.append(task)

    response = temp
    ChatHistory.extend(
        [
            {
                "role": "User",
                "message": f"{prompt}"
            },
            {
                "role": "Chatbot",
                "message": f"{response2}"
            }
        ]
    )
    
    return response, ChatHistory

if __name__ == "__main__":

      while True:
            
            print(FirstLayerDMM(input(">>> "),[]))

