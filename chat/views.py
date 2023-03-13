import json
from django.http import JsonResponse
from revChatGPT.V3 import Chatbot
from anychat.settings import CHATGPT_API_KEY


chatbot = Chatbot(api_key=CHATGPT_API_KEY)

messageType = {
    'message': str,
    'role': str,
}
messagesType = list[messageType]


def index(request) -> JsonResponse:
    """ 请求 chatgpt 的 api """
    if request.method == 'POST':
        messages: messagesType = json.loads(request.body)['messages']
        question = messages.pop()
        for i in range(len(messages)):
            chatbot.add_to_conversation(**messages[i])
        reply = chatbot.ask(question['message'])
        return JsonResponse({'reply': reply})
