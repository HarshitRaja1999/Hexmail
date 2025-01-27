from google.cloud import pubsub_v1
from gmail.gmail_cmnds import service
import os
import json
import asyncio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pub_sub\pub_sub_token.json"

def user_info(id,auth=False):
    file = open('user_info.json','r')
    try:
        user_id = json.loads(file.read())
    except:
        user_id={}
    file.close()
    if str(id) in user_id.keys():
        if 'token' in user_id[str(id)].keys():
            return user_id[str(id)]
        else:
            if auth:return user_id[str(id)]
            else:return "U/A"

USER = user_info(910215301071781939)

request = {
  'labelIds': ['INBOX','SENT',''],
  'topicName': 'projects/gmail-api-testing-331909/topics/Pub-Sub_gmail_API_tesing'
}

subscription_id = "Pub-Sub_gmail_API_tesing-sub"
project_id = "gmail-api-testing-331909"

def save_history_id(id):
    with open('pub_sub\history_list.txt','r') as f:
        a=f.read()
    with open('pub_sub\history_list.txt','w') as f:
        f.write(str(id))
    return a

class PubSub:
    def __init__(self,conn) -> None:
        self.conn = conn
        self.subscriber_func()

    def subscriber_func(self):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        flow_control = pubsub_v1.types.FlowControl(max_messages=10)
        streaming_pull_future = subscriber.subscribe(
            subscription_path, callback=self.callback, flow_control=flow_control
        )
        print(f"Listening for messages on {subscription_path}..\n")
        with subscriber:
            try:
                streaming_pull_future.result()
            except KeyboardInterrupt:
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.
    
    def callback(self,message: pubsub_v1.subscriber.message.Message) -> None:
        message.ack()
        msg = json.loads(message.data.decode("utf-8"))
        self.conn.send(msg)
        # history_id=int(msg['historyId'])
        # new_mail={'email':msg['emailAddress']}
        # history_id = save_history_id(history_id)
        # service_obj = service(USER['token'])
        # new_changes=self.history_list_parse(service_obj.history_list(history_id))
        # new_mail['new_changes'] = new_changes
        # print(new_mail)

    def apply_renew_watch(self,credential):
        # print(service.users().watch(userId='me',body=request).execute())
        pass

    def history_list_parse(self,history_list):
        new_history_id = history_list['historyId']
        save_history_id(new_history_id)
        history = history_list['history']
        messages = {}
        for i in history:
            try:
                a=i['messagesAdded']
                messages[a[0]["message"]['id']]=a[0]['message']['labelIds']
            except Exception as e:
                # print("Error",e)
                pass
        return messages

if __name__=="__main__":
    # print(apply_renew_watch(USER['910215301071781939']['token']))
    obj=PubSub(True)