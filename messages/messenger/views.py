from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from keys import VERIFY_TOKEN, MESSENGER_TOKEN
import requests
from django.views.generic import View
from django.utils.decorators import method_decorator
import json

FB_ENDPOINT = 'https://graph.facebook.com/v15.0/'

class FacebookWebhookView(View):
    @method_decorator(csrf_exempt) # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) #python3.6+ syntax

    def get(self, request, *args, **kwargs):
        hub_mode   = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status_code=403)
        return HttpResponse(hub_challenge)


    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    fb_user_id = message['sender']['id'] # sweet!
                    fb_user_txt = message['message'].get('text')
                    if fb_user_txt:
                        sendMessage(fb_user_id, fb_user_txt)
                    print(f"USER ID: {fb_user_id}\nTEXT: {fb_user_txt}")
        return HttpResponse("Success", status=200)

def sendMessage(fbid, recevied_message):
    # print(recevied_message)
    msg = recevied_message
    if msg is not None:                 
        endpoint = f"{FB_ENDPOINT}/me/messages?access_token={MESSENGER_TOKEN}"
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
        status = requests.post(
            endpoint, 
            headers={"Content-Type": "application/json"},
            data=response_msg)
        print(status.json())
        return status.json()
    return None


# Create your views here.
# @csrf_exempt
# def index(request):
#     if request.method == "GET":
#         print("GETTTT")
#         mode = request.GET['hub.mode']
#         token = request.GET['hub.verify_token']
#         challenge = request.GET['hub.challenge']
#         if mode == 'subscribe' and token == VERIFY_TOKEN:
#             return HttpResponse(challenge, status = 200)
#         else:
#             return HttpResponse('error', status = 403)
#     if request.method == "POST":
#         print("POST MESSAGE")
#         print(request)
#         return HttpResponse("success", status = 200)

# def sendMessengerMessage(request):
#     response = requests.post(
#         f"https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/messages?recipient={'id':'PSID'}&messaging_type=RESPONSE&message={'text':'hello,world'}&access_token={MESSENGER_TOKEN}")
#     print(response)

# import json
# import requests, random, re
# from django.http import HttpResponse, JsonResponse
# from django.views.generic import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# from .logic import LOGIC_RESPONSES


# VERIFY_TOKEN = "7711df715abcfa28ace91507da2d28d907a2d2db3c7c6639b0" # generated above

# FB_ENDPOINT = 'https://graph.facebook.com/v15.0/'
# PAGE_ACCESS_TOKEN = "EAAaYRZC9eX9kBAK8F489D648lp1HDlo55puWX86OPIgBoZBMVZC6viDjnacWau8ZBWVsziyFpmqNRquemZBtrDHKOfwyx2P4fTNQhMdoFGSkANe8We4Wn0do68yKpwL283SR6aZA6yb0QiyrkIe36CtxbqimwO9eOYJFU4Jq5Nbe1dmPUhM6pQ"

# def parse_and_send_fb_message(fbid, recevied_message):
#     # Remove all punctuations, lower case the text and split it based on space
#     tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
#     msg = None
#     for token in tokens:
#         if token in LOGIC_RESPONSES:
#             msg = random.choice(LOGIC_RESPONSES[token])
#             break

#     if msg is not None:                 
#         endpoint = f"{FB_ENDPOINT}/me/messages?access_token={PAGE_ACCESS_TOKEN}"
#         response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
#         status = requests.post(
#             endpoint, 
#             headers={"Content-Type": "application/json"},
#             data=response_msg)
#         print(status.json())
#         return status.json()
#     print("NONE")
#     return None


# class FacebookWebhookView(View):
#     @method_decorator(csrf_exempt) # required
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs) #python3.6+ syntax

#     '''
#     hub.mode
#     hub.verify_token
#     hub.challenge
#     Are all from facebook. We'll discuss soon.
#     '''
#     def get(self, request, *args, **kwargs):
#         hub_mode   = request.GET.get('hub.mode')
#         hub_token = request.GET.get('hub.verify_token')
#         hub_challenge = request.GET.get('hub.challenge')
#         if hub_token != VERIFY_TOKEN:
#             return HttpResponse('Error, invalid token', status_code=403)
#         return HttpResponse(hub_challenge)


#     def post(self, request, *args, **kwargs):
#         incoming_message = json.loads(request.body.decode('utf-8'))
#         for entry in incoming_message['entry']:
#             for message in entry['messaging']:
#                 if 'message' in message:
#                     fb_user_id = message['sender']['id'] # sweet!
#                     fb_user_txt = message['message'].get('text')
#                     if fb_user_txt:
#                         parse_and_send_fb_message(fb_user_id, fb_user_txt)
#         return HttpResponse("Success", status=200)

