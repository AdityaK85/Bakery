#### settings.FIREBASE_NOTIFICATION_URL = 'https://fcm.googleapis.com/fcm/send'
#### settings.FIREBASE_API_KEY = 'AAAALZBX4sQ:APA91bHdutS9emWeiICaE3dnSYngxgxlO8yKURsJymM3KXltrDpPHTnF4qwAqTI3zdzGjwB9F6bvtnpJ7vvuIdY5RaPsa1n41KmLq9wjCNaIFOo01r4X_esMCm10u7SuRSjQnOytTRId'
 
import datetime, traceback, requests, json
from django.conf import settings 

def send_notification(token_list, message_title, message_body, data_message):
    try:
        if (message_title != '' and message_body != '') and (message_title != None  and message_body != None ) and (data_message != '' and data_message != None ):
            if token_list:
                url = settings.FIREBASE_NOTIFICATION_URL 
                payload = {
                    "data" : data_message,
                    "notification" : {
                        "title":message_title,
                        "body":message_body,
                    },
                    "registration_ids":token_list
                }
                headers = {
                    'Authorization':'key='+str(settings.FIREBASE_API_KEY),
                    'Content-Type': 'application/json' 
                }
                response = requests.post(url, headers=headers, data = json.dumps(payload))
                print(response.text)
            else: 
                print('-------------token list is blank-----------------------')
            
        return response.json()['success'] != 0 
    except:
        print(str(traceback.format_exc()))
        return "error"
        

def Send_Message(message_body, job_id,  token_list):
    message_title = 'Kago'
    data_message = {
        'title': message_title,
        "body": message_body,
        "action": "recived",
        "action_id":f"{job_id}" ,
        "current_datetime": str(datetime.datetime.now()).split(".")[0],
        "image_url": "", 
        "android_channel_id": "noti_push_app_2",
        "sound": "alarm.mp3",
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
    } 
    res = send_notification(token_list, message_title, message_body, data_message)
    print("notification response..................",res)
    # print("notification MSG..................",data_message)
    return res            

# print('Hello') 
# Send_Message(OffersDetails.objects.get(id=105))

