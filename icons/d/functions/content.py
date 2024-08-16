
from groq import Groq
import os
from dotenv import get_key


client = Groq(api_key=get_key("CONST","GroqAPIKey"))


def Content(Topic):

    def ContentWriterAI(prompt):
        SystemChatBot = [{"role": "system","content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]
        messages = []
        messages.append({"role": "user", "content": f"{prompt}"})
        completion = client.chat.completions.create(
        model = "mixtral-8x7b-32768",
        messages = SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None)

        Answer =""
        for chunk in completion:
                if chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    return ContentByAI