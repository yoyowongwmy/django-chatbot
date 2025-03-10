from django.urls import path
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [path("chat_session/<int:pk>/", views.chat_session)]


urlpatterns = format_suffix_patterns(urlpatterns)