from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse

from chat import models


class ChatMessageSerializer(serializers.ModelSerializer):
    receiver = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field='username'
    )
    sender = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = models.ChatMessage
        fields = ('message', 'receiver', 'sender', 'created_at')
        read_only_fields = ('created_at', 'sender')

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super(ChatMessageSerializer, self).create(validated_data)


class UsersListSerializer(serializers.ModelSerializer):
    chat_url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'chat_url')

    def get_chat_url(self, instance):
        return reverse('chatmessage-detail', args=[instance.username])
