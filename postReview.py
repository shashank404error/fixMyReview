from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import configManager 

def post_reply(review_id, reply_text):
    try:
        credentials = Credentials.from_service_account_file(
            configManager.SERVICE_ACCOUNT_FILE,
            scopes=configManager.ANDROID_PUBLISHER_API_SCOPE
        )

        service = build(configManager.SERVICE_NAME_ANDROID_PUBLISHER, configManager.ANDROID_PUBLISHER_API_VERSION, credentials=credentials)

        body = {"replyText": reply_text}

        response = service.reviews().reply(
            packageName=configManager.APP_PACKAGE_NAME,
            reviewId=review_id,
            body=body
        ).execute()

        print(f"==> Reply posted successfully: {response}\n")
        return 1
    except Exception as e:
        print(f"^^^ An error occurred: {e}\n")
        return 0
