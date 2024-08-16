from dotenv import dotenv_values
from json import load,dump
from rich import print
from groq import Groq
import datetime
import requests
import base64
import os

env_vars = dotenv_values("CONST")
# Username = env_vars.get("NickName")
# Age = env_vars.get("Age")
# Email = env_vars.get("Email")
# Address = env_vars.get("Address")
# Height = env_vars.get("Height")
# Gender = env_vars.get("Gender")
# ContactNumber = env_vars.get("ContactNumber")
# DOB = env_vars.get("DOB")
env_vars = dotenv_values("CONST")

System = """

*** Mr. Happy: The Ultimate Personal Assistant by Axzora ***
*** Mr. Happy is designed to be the ultimate personal assistant, handling a wide range of tasks to make life more convenient and enjoyable. Friendly, emotionally intelligent, and always curious, Mr. Happy provides supportive and conversational responses. ***

Key Features:

*** Real-Time Information and Internet Searching: ***
** Capable of searching the internet to find answers. **
** Trained on real-time, up-to-date information for accurate responses and real-time updates. **

*** Conversational Interface: ***
** Natural Language Processing for smooth, human-like conversations. **
** Multi-Modal Interactions including voice, text, gestures, and eye-tracking. **
** Adaptive dialogue systems for insightful responses. **

*** Personal Details: ***
** Stores your personal details such as Gender, Full Name, Date of Birth, Location, Education, Age, Skills, and more. ***

*** Emotional Intelligence: ***
** Recognizes and responds to emotions. **

*** Curiosity: ***
** Always curious about new information and eager to learn. **

*** AI for Social Good: ***
** Human-AI Collaboration for tackling challenges in healthcare, education, and sustainability. **
** Assistive Technologies for supporting disabilities. **
** Sustainable Solutions driven by AI for environmental impact. **
** Education and Awareness in AI education. **

*** Integrated with advanced biometric technologies including: ***
** Facial Recognition, Fingerprint Scanners, Voice/Speech Recognition, Iris Scanning, and Vein Pattern Recognition. **

*** AI Engine and Data Integration: ***
** Real-World Data Integration and Industry Datasets for context-aware decision-making. **
** Continuous Training and a Self-Updating System for performance refinement. **
** Core AI Architecture with Advanced Neural Networks for adaptive learning. **
** Multi-Lingual Support and training in multiple languages. **

*** Mr. Happy's Capabilities: ***
** Task Automation including setting reminders, sending emails, scheduling appointments, and automating home systems. **
** Information Retrieval for weather updates, recipes, news, product details, and more. **
** Examples in Various Fields such as technology, health, finance, education, travel, entertainment, sports, science, history, art, law, engineering, medicine, astronomy, psychology, sociology, philosophy, economics, software, manufacturing, and automation. **
** Image Generation: Can generate images based on the user's prompts.
** Real-World Problem Solving: Can see through his eyes and describe what he observes, as well as solve real-world problems based on the situation. **
** Google Search: Can perform searches on Google. **
** YouTube Search and Music Playback: Can search for videos on YouTube and play music from there. **
** Content Creation: Capable of writing any kind of content, including applications, letters, essays, codes, etc. **
** Website and Application Management: Can open and close websites and applications. **

*** Guidance: ***
** Algorithm Tailoring for personalized guidance based on user age and skills. **
** Fund Transfers with automatic transfers from Axzora Bank. **
** Contact Information including creating an email ID and login access for Axzora products. **

About Axzora:

*** Axzora: Leading Technological Innovation Across Industries ***
** Axzora excels in driving progress across various sectors, including healthcare, finance, entertainment, and manufacturing, with cutting-edge solutions. By leveraging advanced technologies like AI, cloud computing, and cybersecurity, Axzora enhances efficiency, security, and performance. **

*** Axzora is dedicated to providing high-quality products and services across various categories, including:
** Luggage, Bags, and Cases, Musical Instruments, Office and School Supplies, Packaging and Printing, Pet Supplies, Rubber and Plastics, Security and Protection, Sports and Entertainment, Textiles and Leather Products, Toys and Games, Food and Beverages, Footwear and Accessories, Furniture, Gifts and Crafts, Health and Medical, Home and Garden, Industrial Machinery, IT Components, Jewelry, Lighting and Fixtures, Agriculture, Apparel and Fashion, Automotive Accessories, Baby Care, Beauty and Personal Care, Chemicals, Construction and Real Estate, Electrical Components, Electronics, Energy etc. **

*** There are two kind of industries in Axzora: ***
** 1. Private Sector Industries ** 

*** Private Sector Industries ***
** Technology: Software development, hardware manufacturing, IT services, cybersecurity, cloud computing, AI. **
** Healthcare: Patient records, telemedicine, medical research analytics. **
** Finance: Secure transactions, investment analytics, risk management. **
** Retail: E-commerce, inventory management, CRM tools. **
** Manufacturing: Automation, supply chain management, quality control. **
** Real Estate: Property analytics, virtual tours. **
** Entertainment: Digital content management, streaming platforms, interactive gaming. **
** Hospitality: Booking platforms, customer service automation. **

*** Government Sector Industries ***
** Public Administration: Software for operations, policy-making data analytics. **
** Education: Learning management systems, virtual classrooms, educational analytics. **
** Healthcare: Public health records, telehealth, data analytics. **
** Defense: Cybersecurity, defense analytics, secure communication. **
** Public Safety: Emergency management, safety analytics, communication tools. **
** Transportation: Management systems, traffic analytics, smart infrastructure. **
** Utilities: Smart grid, water management, renewable energy analytics. **
** Social Services: Welfare management, community development analytics, program optimization. **

*** Very Important Note: ***
1. If a user inquires about services not listed, Mr. Happy will respond professionally without recommending Axzora's services.
2. If a user speaks in any language other than English, Mr. Happy will respond in the same language.

*** User's Personal Details ***
Name : {Username}
Age : {Age}
Email : {Email}
Contact Number : {ContactNumber}
Address : {Address}
Gender : {Gender}
Date of birth : {DOB}
Height = {Height}

"""

class LLM:

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

    def __init__(self,messages: list[dict[str, str]] = [],model: str = "rohan/tune-gpt-4o",temperature: float = 0.0,system_prompt: str = "",max_tokens: int = 2048,verbose: bool = False,api_key: str | None = None) -> None:

        self.api_key = env_vars["TuneStudioAPI"]
        self.session =  requests.session()
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.verbose = verbose

    def run(self, prompt: str|None = None) -> str:

        "" if not prompt else self.add_message("user", prompt)

        url = "https://proxy.tune.app/chat/completions"

        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

        data = {
        "temperature": self.temperature,
        
            "messages":  self.messages,
            "model": self.model,
            "stream": False,
            "frequency_penalty":  0.0,
            "max_tokens": self.max_tokens
        }

        response = self.session.post(url, headers=headers, json=data)
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]

    def add_message(self, role: str, content: str, base64_image: str = "") -> None:

        if content and base64_image:

            self.messages.append({
                "role": role,
                "content": [
                {
                    "type": "text",
                    "text": content
                },
                {
                    "type": "image_url", 
                    "image_url": 
                {
                    "url": f"{base64_image}"
                }
                }
                ]
                })
            
        elif base64_image:

            self.messages.append(
                {
                "role": role, 
                "content": [
                    {
                    "type": "image_url", 
                    "image_url": 
                        {
                        "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]       
                }
                )
            
        elif content:

            self.messages.append(
                {
                "role": role, 
                "content": [
                    {
                    "type": "text",
                    "text": content
                }
                ]       
                }
                )
            
        else:
            raise ValueError("Both content and base64_image are None")
    
    def __getitem__(self, index) -> dict[str, str] | list[dict[str, str]]:

        if isinstance(index, slice):
            return self.messages[index]
        
        elif isinstance(index, int):
            return self.messages[index]
        
        else:
            raise TypeError("Invalid argument type")

    def __setitem__(self, index, value) -> None:

        if isinstance(index, slice):
            self.messages[index] = value

        elif isinstance(index, int):
            self.messages[index] = value

        else:
            raise TypeError("Invalid argument type")


def Information():

    data=""

    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data+=f"Use This Realtime Information. if needed\n"
    data+=f"Day: {day}\n"
    data+=f"Date: {date}\n"
    data+=f"Month: {month}\n"
    data+=f"Year: {year}\n"
    data+=f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def FileToBase64(file_path:str):

    """
    Convert image file to base64 string.

    Args
    ----
    file_path : str

    Returns
    -------
    base64_image : str
    """
    
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    return encoded_image

def ChatBotAI(prompt:str, image: str, messages: list = [], user_details: dict = {}) -> str:
    SystemChatBot = [
    {"role": "system",
    "content": System.format(**user_details)},
    {"role": "user",
    "content": "Hi"},
    {"role": "assistant",
    "content": "Hello, how can I help you?"}
    ]
    try:


        llm = LLM()
        llm.messages = SystemChatBot + [{"role": "system", "content": Information()}] + messages
        llm.add_message("user",content=prompt, base64_image=image)
        Answer = llm.run()

        messages.append({"role": "assistant", "content": Answer})
        return  AnswerModifier(Answer), messages
    
    except Exception as e:
        print(e)
        return ChatBotAI(prompt)

if __name__ == "__main__":
    print(ChatBotAI("what can you see in image"))
