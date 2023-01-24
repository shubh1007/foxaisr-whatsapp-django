from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import random
from messages.settings import WHATSAPP_TOKEN, VERIFY_TOKEN
from .models import MessageTemplate

# Create your views here.
def generateOTP():
    message = " is your OTP for Foxaisr.\nDo not share your OTP with anyone.\nDon't Reply on this number.\nOur World Class Website: https://www.foxaisr.com/"
    OTP = ""
    for _ in range(6):
        OTP += str(random.randrange(0, 9))
    message = OTP + message
    return message

def sendOTP(request):
    if request.method == "GET":
        message = generateOTP()
        phoneNumber = "917098213317"
        message = sendWhatsAppMessage(phoneNumber, message)
        return render(request, "index.html")
    elif request.method == "POST":
        print("Inside POST")
        message = request.POST.get("Body")
        phoneNumber = "917098213317"
        message = sendWhatsAppMessage(phoneNumber, message)
        return render(request, 'index.html', {"prompt": "POSTED!"})

def addTemplate(request):
    templates = MessageTemplate.objects.all()
    context = {"templates": templates}
    if request.method == "POST":
        name = request.POST.get("name")
        template = request.POST.get("template")
        p = MessageTemplate(name = name, message = template)
        p.save()
        return render(request, 'template.html', context)
    elif request.method == "GET":
        return render(request, 'template.html', context)

def sendWhatsAppMessage(phoneNumber, message):
    headers = {"Authorization": WHATSAPP_TOKEN}
    headers["Content-Type"] = "application/json"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post("https://graph.facebook.com/v15.0/111909698452771/messages", headers=headers, json=payload)
    ans = response.json()
    return ans

# message = "Hello World This is Shubham Kumar Sharma! Hope You are Doing Fine"
# ans = sendWhatsAppMessage(message)
# print(ans)

@csrf_exempt
def whatsAppWebHook(request):
    if request.method == "GET":
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status = 200)
        else:
            return HttpResponse('error', status = 403)
    if request.method == "POST":
        # print("recieved messages")
        data = json.loads(request.body)
        print(data)
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                        # phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
                        # profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        # whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        # fromId = entry['changes'][0]['value']['messages'][0]['from']
                        # messageID = entry['changes'][0]['value']['messages'][0]['id']
                        # timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                        if entry:
                            text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        message = f"RE: ```{text}``` was received"
                        print(message)
                        phoneNumber = "917098213317"
                        message = sendWhatsAppMessage(phoneNumber, message)
                        print(message)
                except:
                    pass
        return HttpResponse("success", status = 200)


{
    'id': '107496555565289', 
    'changes': [
        {'value': {
            'messaging_product': 'whatsapp', 
            'metadata': {
                'display_phone_number': '15550350359', 
                'phone_number_id': '111909698452771'
                }, 
            'contacts': [{'profile': {'name': 'Shubham'}, 'wa_id': '917098213317'}], 

            'messages': [
                {
                    'from': '917098213317', 
                    'id': 'wamid.HBgMOTE3MDk4MjEzMzE3FQIAEhgUM0VCMDQ4RkYxQjkzOTlENTgwRkQA', 
                    'timestamp': '1673637195', 
                    'text': {
                        'body': 'hey'
                        }, 
                    'type': 'text'
                }
            ]
        }, 
        'field': 'messages'
        }
    ]
}