from __future__ import print_function
import logging
from google_auth_oauthlib.flow import Flow

# If modifying these scopes, delete the file credentials.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
APPLICATION_NAME = "Gmail-API-testing"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

def get_authorization_url():
    """
    It gets an url from gmail api which will open user gmail
        for permission to authorize the app to access the emails.
    Returns: 
        A url for authorization of this app to gmail api.
    """
    flow = Flow.from_client_secrets_file(
        'gmail\credentials.json',
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url,_ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return authorization_url

def get_credentials(authorization_code=None):
    """Exchange an authorization code for OAuth 2.0 credentials.
    Args:
        authorization_code: Authorization code to exchange for OAuth 2.0
                            credentials.
    Returns:
        oauth2client.client.OAuth2Credentials instance.
    Raises:
        CodeExchangeException: an error occurred.
    """
    flow = Flow.from_client_secrets_file(
        'gmail\credentials.json',
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    try:
        flow.fetch_token(code=authorization_code)
        return flow.credentials
    except Exception as error:
        logging.error('An error occurred: %s', error)

if __name__ == '__main__':
    url = get_authorization_url()
    print(url)
    code = input('Please input authorization code : ')
    credentials = get_credentials(authorization_code=code)


#Labels:
# CHAT
# SENT
# INBOX
# IMPORTANT
# TRASH
# DRAFT
# SPAM
# CATEGORY_FORUMS
# CATEGORY_UPDATES
# CATEGORY_PERSONAL
# CATEGORY_PROMOTIONS
# CATEGORY_SOCIAL
# STARRED
# UNREAD
# Personal
# Receipts
# Work