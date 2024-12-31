from google.oauth2 import service_account
from googleapiclient.discovery import build
import configManager 
from generateResponse import generate_reply,trim_reply
from postReview import post_reply

credentials = service_account.Credentials.from_service_account_file(
    configManager.SERVICE_ACCOUNT_FILE, scopes = configManager.ANDROID_PUBLISHER_API_SCOPE
)

service = build(configManager.SERVICE_NAME_ANDROID_PUBLISHER, configManager.ANDROID_PUBLISHER_API_VERSION, credentials=credentials)

def fetch_all_reviews(batchCount):
    try:
        reviews = []
        next_page_token = ""

        # Fetch all the reviews
        for idx in range(batchCount):
            print("==> Fetching review for batch "+str(idx+1)+"\n")
            
            request = service.reviews().list(
                packageName=configManager.APP_PACKAGE_NAME,
                maxResults=100,
                token=next_page_token
            )
            response = request.execute()

            reviews.extend(response.get('reviews', []))

            next_page_token = response.get('tokenPagination', {}).get('nextPageToken')
            if not next_page_token:
                print("==> no more reviews found\n")
                break

        # Process reviews
        for review in reviews:
            review_id = review['reviewId']
            review_text = review.get('comments', [{}])[0].get('userComment', {}).get('text', 'No text')
            
            reply = False
            if len(review['comments'])>1:
                replyText = review['comments'][1]['developerComment']['text']
                if replyText != None:
                    reply = True

            if reply:
                print(f"==> [REPLIED][SKIPPING] Review ID: {review_id} Reply: [{replyText}]\n")
                continue
            
            else:                
                print(f"==> [NOT REPLIED] Review ID: {review_id} Review: [{review_text}]\n")
                
                firstName = review['authorName']
                nameArr=str.split(review['authorName'])
                if len(nameArr)>1:
                    firstName = nameArr[0]
                
                agentReply=generate_reply(review_text,firstName,review['comments'][0]['userComment']['starRating'])
                
                if agentReply=="":
                    print(f"^^^ Some issue in agent reply\n")
                    continue
                print(f"==> [AGENT]: [{agentReply}] WordCount: [{len(agentReply)}]\n")
                
                # Post the reply only if it's less than 350 character (playstore limit)
                if len(agentReply)<350:
                    user_input = 1
                    if configManager.IS_AUTO_PILOT_MODE_ON==False:
                        user_input = input("@@@ Press 1 to post this reply: ")
                    
                    ## A fail safe to let the executer in control
                    if user_input=="1":
                        print("==> Going to post this reply")
                        resp = post_reply(review_id,agentReply)
                        if resp==0:
                            continue
                    else:
                        print("==> Skipping this review\n")
                        continue

                # Process the reply again to bring it under 350 character limit
                else:                    
                    while True:
                        diffCount = len(agentReply) - 350
                        agentReply=trim_reply(agentReply,diffCount)
                        if agentReply=="":
                            print(f"==> Some issue in agent reply\n")
                            continue
                        print(f"==> [TRIMMED AGENT]: [{agentReply}] WordCount: [{len(agentReply)}]\n")
                        if len(agentReply)<350:

                            user_input = 1
                            if configManager.IS_AUTO_PILOT_MODE_ON==False:
                                user_input = input("@@@ Press 1 to post this trimmed reply: ")
                            if user_input=="1":
                                print("==> Going to post this trimmed reply")
                                resp = post_reply(review_id,agentReply)
                            else:
                                print("==> Skipping this review\n")
                            break

                


    except Exception as e:
        print(f"^^^ An error occurred: {e}")


## call the function to invoke
fetch_all_reviews(configManager.TOTAL_BATCH_API_MODE)
