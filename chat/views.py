from time import sleep

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action


from chat import models, serializers


@login_required
def chat(request):
    context = {
        'users': get_user_model().objects.exclude(id=request.user.id)
    }
    return render(request, 'chat.html', context)


class ChatMessagesViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):

    lookup_field = 'receiver'
    queryset = models.ChatMessage.objects.none()
    serializer_class = serializers.ChatMessageSerializer
    filterset_fields = ['is_read']

    def retrieve(self, request, **kwargs):
        receiver = get_user_model().objects.filter(username=kwargs['receiver']).first()
        if receiver is None:
            return Response([])

        queryset = models.ChatMessage.objects.filter(
            Q(sender=request.user, receiver=receiver) |
            Q(sender=receiver, receiver=request.user)
        ).order_by('-created_at')

        queryset = self.filter_queryset(queryset)

        # TODO: pagination
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data

        unread_message_ids = queryset.filter(is_read=False).values_list('id', flat=True)
        models.ChatMessage.objects.filter(id__in=unread_message_ids).update(is_read=True)

        return Response(serializer_data)

    @action(methods=['GET'], detail=False)
    def stats(self, request):
        now = timezone.now()
        count = 0
        new_messages_exists = self.is_new_messages_exists(now, request.user)
        while (not new_messages_exists) and count < 14:
            sleep(2)
            count += 1
            new_messages_exists = self.is_new_messages_exists(now, request.user)
        unread_count = self.get_unread_count(request.user)
        return Response(dict(unread_count))

    @staticmethod
    def get_unread_count(receiver):
        return models.ChatMessage.objects.filter(
            is_read=False, receiver=receiver
        ).values_list('sender__username').annotate(
            count=Count("id")
        )

    @staticmethod
    def is_new_messages_exists(now, receiver):
        return models.ChatMessage.objects.filter(
            created_at__gte=now,
            receiver=receiver
        ).exists()


class UserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'user.html'
    form_class = UserCreationForm
    success_url = '/'


class UserListViewSet(GenericViewSet, ListModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UsersListSerializer
