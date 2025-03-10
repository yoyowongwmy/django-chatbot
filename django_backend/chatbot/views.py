# from django.shortcuts import render
# from django.http import JsonResponse

# from dotenv import load_dotenv
# import os

# from openai import OpenAI

# from .models import ChatSession

# load_dotenv(override=True)
# openai_api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_api_key)


# def format_message(role: str, text: str) -> dict:
#     """
#     format the message based on openai API doc
#     ref: https://platform.openai.com/docs/guides/text-generation
#     """
#     return {"role": role, "content": [{"type": "text", "text": text}]}


# def ask_openai(messages):
#     """
#     query the openai API
#     ref: https://platform.openai.com/docs/guides/text-generation
#     """
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         temperature=0.7,
#     )
#     answer = response.choices[
#         0
#     ].message.content  # retrieve only the openai message response
#     return answer


# def chatbot(request):
#     """
#     Handle chatbot interactions via GET and POST requests.
#     Persist the user messages and openai responses to session conversation,
#     identified by session id.

#     Args:
#         request (HttpRequest): The HTTP request object.
#     Returns:
#         JsonResponse: A JSON response containing the user message and the assistant's response (for POST requests).
#         HttpResponse: An HTML response rendering the chatbot page (for GET requests).
#     """
#     session_id = request.headers.get("Session-Id", "")
#     chat_session, created = ChatSession.objects.get_or_create(
#         session_id=session_id
#     )  # persist Chat Session in db with the session ID

#     if request.method == "POST":
#         text = request.POST.get("message")

#         # Format user message and add to Chat Session
#         message = format_message(role="user", text=text)
#         chat_session.conversation.append(message)

#         # Format messages argument for openai API call
#         messages = chat_session.conversation + [message]

#         # get response from open ai and add it to Chat Session
#         response = ask_openai(messages)
#         response_message = format_message(role="assistant", text=response)

#         chat_session.conversation.append(response_message)

#         # Persist the updated session data
#         chat_session.save()

#         return JsonResponse({"message": message, "response": response})

#         # Detect AJAX request
#     if request.headers.get("X-Requested-With") == "XMLHttpRequest":
#         return JsonResponse({"conversation": chat_session.conversation})

#     return render(request, "chatbot.html")


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def format_message(role: str, text: str) -> dict:
    """
    format the message based on openai API doc
    ref: https://platform.openai.com/docs/guides/text-generation
    """
    return {"role": role, "content": [{"type": "text", "text": text}]}

def ask_openai(messages):
    """
    query the openai API
    ref: https://platform.openai.com/docs/guides/text-generation
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )
    answer = response.choices[
        0
    ].message.content  # retrieve only the openai message response
    return answer

@api_view(['GET', 'POST', 'DELETE'])
def chat_session(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    # try:
    #     chatSession = ChatSession.objects.get(session_id=pk)
    # except ChatSession.DoesNotExist:
    #     chatSession = ChatSession.objects.create(session_id=pk)
    chatSession, created = ChatSession.objects.update_or_create(session_id=pk)
    
    if request.method == 'POST':
        message = format_message(role="user",text=request.data.get("message"))
        chatSession.conversation.append(message)
        
        messages = chatSession.conversation + [message]
        answer = ask_openai(messages)
        response = format_message(role="assistant",text=answer)
        chatSession.conversation.append(response)
        
        chatSession.save()
                
        serializer = ChatSessionSerializer(chatSession)
        return Response(serializer.data)   
    
    elif request.method == 'GET':
        serializer = ChatSessionSerializer(chatSession)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        chatSession.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
