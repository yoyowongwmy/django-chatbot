from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

history_messages = [] # global variable to store all the messages received. 

def format_message(role:str, text:str) -> dict:
    return {"role": role, "content": [{"type": "text", "text": text}]}


def ask_openai(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.7,
    )
    answer = response.choices[0].message.content
    return answer

def chatbot(request):
    if request.method == "POST":
        text = request.POST.get("message")
        # response = "Hello, you said: " + message
        message = {"role": "user", "content": [{"type": "text", "text": text}]}
        history_messages.append(message)
        response = ask_openai(history_messages)
        response_message = format_message(role="assistant",text=response)
        history_messages.append(response_message)
        print(history_messages)
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html")
