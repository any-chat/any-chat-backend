from django.urls import path
from chat import views as chat


urlpatterns = [
    path('', chat.index, name='chat_index'),
]
