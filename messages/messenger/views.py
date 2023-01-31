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
        """
            The view part of the view – 
            the method that accepts a request argument plus arguments, 
            and returns an HTTP response.

            The default implementation will inspect the HTTP method 
            and attempt to delegate[meaning: representative] to a method that matches the HTTP method; 
            a GET will be delegated to get(), a POST to post(), and so on.

            By default, a HEAD request will be delegated to get(). 
            If you need to handle HEAD requests in a different way than GET, 
            you can override the head() method. 
            See Supporting other HTTP methods for an example.

        Args:
            request : request 
            *args[Optional]: parameters
            **kwargs[Optional]: parameters

        Returns:
            request: redirect to suitable method[GET/POST]
            *args[Optional]: parameters
            **kwargs[Optional]: parameters
        """
        return super().dispatch(request, *args, **kwargs) #python3.6+ syntax

    def get(self, request, *args, **kwargs):
        hub_mode   = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status=403)
        return HttpResponse(hub_challenge, status = 200)
    # @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))
        print(incoming_message)
        psid = incoming_message['entry'][0]['messaging'][0]['sender']['id']
        prid = incoming_message['entry'][0]['messaging'][0]['recipient']['id']
        temp = incoming_message['entry'][0]['messaging'][0]
        if temp.get('message'):
            message = temp['message'].get("text")
            sendMessage(psid, message)
        
        # for entry in incoming_message['entry']:
        #     for message in entry['messaging']:
        #         if 'message' in message:
        #             fb_user_id = message['sender']['id'] # sweet!
        #             fb_user_txt = message['message'].get('text')
        #             if fb_user_txt:
        #                 sendMessage(fb_user_id, fb_user_txt)
        #             print(f"USER ID: {fb_user_id}\nTEXT: {fb_user_txt}")
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
        # print(status.json())
        print("Send Message Method")
        return status.json()
    return None

