from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def ask_openai(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    print(response)
    answer = response.choices[0].message.content
    return answer


def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message")
        # response = "Hello, you said: " + message
        messages = [
            {
                "role": "developer",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a helpful assistant that answers programming \
                    questions in the style of a southern belle from the \
                    southeast United States.",
                    }
                ],
            },
            {"role": "user", "content": [{"type": "text", "text": message}]},
        ]
        response = ask_openai(messages)
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html")
