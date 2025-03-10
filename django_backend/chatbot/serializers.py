from rest_framework import serializers
from .models import ChatSession


class ChatSessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatSession
        fields = ["session_id", "created", "conversation"]

    def update(self, instance, validated_data):
        """
        Update and return an existing `ChatSession` instance, given the validated data.
        """
        instance.conversation.append(validated_data.get("message", []))
        instance.save()
        return instance
