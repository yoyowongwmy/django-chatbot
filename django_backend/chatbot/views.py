from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

history_messages = [] # global variable to store all the messages received. 
session_store = {}

my_assistant = client.beta.assistants.create(
    instructions="You are a personal programming tutor. When asked a question, write and run Python code to answer the question.",
    name="Programming Tutor",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo",
)



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

from django.http import JsonResponse
from .models import ChatSession

def format_message(role: str, text: str) -> dict:
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
    # Get session_id from headers
    session_id = request.headers.get("Session-Id", "")
    if not session_id:
        return JsonResponse({"error": "Session ID missing"}, status=400)

    # Retrieve or create the chat session
    chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)

    if request.method == "GET":
        # Return the current conversation history
        return JsonResponse({"conversation": chat_session.conversation})

    if request.method == "POST":
        text = request.POST.get("message")
        if not text:
            return JsonResponse({"error": "Message content missing"}, status=400)

        # Append user message to the conversation history
        user_message = format_message(role="user", text=text)
        chat_session.conversation.append(user_message)
        
        # Prepare messages for OpenAI API
        messages = [{"role": "user", "content": [{"type": "text", "text": text}]}]

        # Get response from OpenAI
        response = ask_openai(messages)
        response_message = format_message(role="assistant", text=response)
        
        # Append assistant response to the conversation history
        chat_session.conversation.append(response_message)
        
        # Save the updated session data
        chat_session.save()

        return JsonResponse({"message": user_message, "response": response})

    return JsonResponse({"error": "Invalid method"}, status=405)


# def chatbot(request):
    
#     if request.method == "GET":
#         session_id = request.headers.get("Session-Id", "")  # Get session ID from headers (not POST)
#         chat_history = session_store.get(session_id, [])

#     if request.method == "POST":
#         text = request.POST.get("message")
#         session_id = request.headers.get("Session-Id", "")  # Get session ID from headers
#         if not session_id:
#             return JsonResponse({"error": "Session ID missing"}, status=400)
#         if session_id not in session_store:
#             session_store[session_id] = []  # Initialize chat history for this session
        
#         chat_history = session_store.get(session_id, [])
#         # Format user message and add to chat history
#         message = format_message(role="user",text=text)
#         chat_history.append(message) # add message to session chat history
        
#         messages= chat_history + [message]
        
#         # get response from open ai and add it to session chat history
#         response = ask_openai(messages)
#         response_message = format_message(role="assistant",text=response)
#         chat_history.append(response_message)
#         session_store[session_id] = chat_history
        
#         print(session_store)
#         return JsonResponse({"message": message, "response": response})
#     return render(request, "chatbot.html", {"chats": chat_history or []})


# def chatbot(request):
#     if request.method == "POST":
#         text = request.POST.get("message")
        
#         # Format user message and add to chat history
#         message = format_message(role="user",text=text)
        
#         request.session["chat_history"].append(message)
#         messages=[msg for msg in request.session["chat_history"]] + [message]
        

        
#         # get response from open ai and add it to session chat history
#         response = ask_openai(messages)
#         response_message = format_message(role="assistant",text=response)
        
#         request.session["chat_history"].append(response_message)
#         request.session.modified = True  # Ensure Django saves session updates
#         print(session_store)
#         return JsonResponse({"message": message, "response": response})
#     return render(request, "chatbot.html", {"chats": request.session["chat_history"]})
