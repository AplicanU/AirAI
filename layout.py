import chainlit as cl
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

 # Load the API key from the .env file
load_dotenv()
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-4",
    "temperature": 0,
    # ... more settings
}


#Disctionary to define questions
initial_questions = {
    "humidity": "What is the Relative Humidity(RH) in your area? (in percentage)",
    "windSpeed": "What is the average wind speed in your area? (in km/hr)",
    "temperature": "What is the average temperature in your area? (in degree Celsius)",
}

# Dictionary to store user answers
user_answers = {
    "humidity": None,
    "windSpeed": None,
    "temperature": None,
} 
    
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are an expert in Water harvesting techniques from Air. Always answer the user query with factual knowledge. You must present the answer in bullet points with clear headings.",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()

async def conversation():
    # Iterate over questions
    for key, question in initial_questions.items():
        answer = await cl.AskUserMessage(content=question,timeout=180).send()
        user_answers[key] = answer['output'] if answer else None

    # Storing user answers in variables
    humidity =  user_answers["humidity"]
    windSpeed = user_answers["windSpeed"]
    temperature = user_answers["temperature"]

    print(humidity, windSpeed, temperature)
    await cl.Message(content="Please wait while I am finding the related information for you.").send()

    first_user_query = "Please let me know the average water generated against " + temperature + " degree Celsius , against Average RH of " + humidity + " percent and against average wind of " + windSpeed + " Km/hour."

    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are an expert in Water harvesting techniques from Air. Answer the user queries based on studies and data related to Air to Water generation techniques. ##You must provide to the point answer in 2 lines without mentioned any other details. //If the provided temperature is greater than or equal to 25 degree celsius, provide the answer for Air to Water Generator (AWG) else if the provided temperature is below 25 degree Celsius, provide the answer for 48 square meter of Fog mesh water generator.",
                "role": "system"
            },
            {
                "content": first_user_query,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()










@cl.on_chat_start
async def main():
    await cl.Avatar(
        name="Air AI",
        url="public/favicon.png",
    ).send()
    await cl.Avatar(
        name="You",
        url="public/user_icon.png",
    ).send()
    content1 = "Hello, welcome to Air AI. We can help providing you answer on how you can extract water from air and use it for agriculture. \n Please help me with the following parameters."
    await cl.Message(content=content1).send()
    response = await conversation()
    
