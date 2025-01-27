from __future__ import print_function
import logging
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from extra_functions import parse_mail
import logging

class service:
    def __init__(self,credential) -> None:
        self.service=self.build_service(credential)

    def build_service(self,credential):
        """
        Builds a gmail service
        Args:
            credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                        request.
            id: users discord Id.
        Returns:
            A gamil service which helps us in retriving info from gmail.
        """
        creds=Credentials.from_authorized_user_info(info=credential)
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return build(serviceName='gmail', version='v1', credentials=creds)
        except:
            return False

    def get_profile(self,for_user_token=False):
        """Send a request to the UserInfo API to retrieve the user's information.
        Args:
            credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                        request.
        Returns:
            User information as a dict.
        """
        user_info=None
        try:
            user_info = self.service.users().getProfile(userId='me').execute()
            if for_user_token:return user_info
            unread = self.service.users().labels().get(userId='me',id='UNREAD').execute()
            msg=f"""Email Address: {user_info['emailAddress']}
            Message Total: {user_info['messagesTotal']}
            Unread Messages Total: {unread['messagesTotal']}
            Threads Total: {user_info['threadsTotal']}
            History Id: {user_info['historyId']}"""
        except Exception as error:
            logging.error('An error occurred: %s', error)
        return msg

    def search_email(self,search_string):
        return self.service.users().messages().list(userId='me',q=search_string).execute()

    def get_emails(self,maxresult=1):
        """Send a request to the UserInfo API to retrieve the user's information.
        Args:
            credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                        request.
            maxresult: maximum number of result a user want to retrieve.
        Returns:
            A dictionary with emails basic info.(NOT THE CONTENT OF EMAILS)
        """
        result = self.service.users().messages().list(maxResults=maxresult,userId='me',labelIds=['INBOX']).execute()
        return result['messages']

    def get_message(self,Id,snippet=False):
        """Send a request to the UserInfo API to retrieve the user's information.
        Args:
            credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                        request.
            snippet: True if the user want the body of the email else False.
        Returns:
            A dictionary with emails info depending upon the value of snippet variable.
        """
        try:
            msg_str = self.service.users().messages().get(userId='me',id=Id,format='full').execute()
            payld = msg_str['payload'] # get payload of the message 
            content={}
            for i in payld['headers']:
                if i['name'] in ['Subject','From','Date']:content[i['name']]=i['value']
            content["snippet"]="".join([i if ord(i) < 128 else '' for i in msg_str['snippet']])
            if snippet:
                try:
                    content['body'] = parse_mail(payld)
                except Exception as e:print("Error in body :",e)
            return content
        except Exception as error:
            print('An error occured: %s'%error)

    def history_list(self,start_history_id):
        return self.service.users().history().list(userId='me',startHistoryId=start_history_id).execute()