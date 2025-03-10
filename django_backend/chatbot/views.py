from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatSession
from .serializers import ChatSessionSerializer

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


@api_view(["GET", "POST", "DELETE"])
def chat_session(request, pk):
    """
    Create, update or delete a chat session.
    """
    chatSession, created = ChatSession.objects.update_or_create(session_id=pk)

    if request.method == "POST":
        # create and add user message to chat session
        message = format_message(role="user", text=request.data.get("message"))
        chatSession.conversation.append(message)
        
        # combine the conversation context and ask open ai
        messages = chatSession.conversation + [message]
        answer = ask_openai(messages)
        
        # create and add system response to chat session
        response = format_message(role="assistant", text=answer)
        chatSession.conversation.append(response)
        
        # persist the change to chat session
        chatSession.save()

        serializer = ChatSessionSerializer(chatSession)
        return Response(serializer.data)

    elif request.method == "GET":
        serializer = ChatSessionSerializer(chatSession)
        return Response(serializer.data)

    elif request.method == "DELETE":
        chatSession.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
