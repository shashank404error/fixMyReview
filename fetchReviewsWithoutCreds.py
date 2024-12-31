from google_play_scraper import reviews, Sort
from generateResponse import generate_reply,trim_reply
from postReview import post_reply
import json
import configManager

def fetch_app_reviews(app_id, count=10, itr=5):
    try:
        
        reviews_list = []

        print("==> Fetching review for first batch")
        result, continuation_token = reviews(
            app_id,
            sort=Sort.NEWEST,
            count=count
        )    
        
        
        for review in result:
            # fetching reviews which are not replied to yet
            if review['replyContent']==None:

                    firstName = review['userName']
                    nameArr=str.split(review['userName'])
                    if len(nameArr)>1:
                        firstName = nameArr[0]

                    reviews_list.append({
                    'reviewId':review['reviewId'],
                    'user': review['userName'],
                    'firstName':firstName,
                    'rating': review['score'],
                    'content': review['content'],
                    'date': review['at'].strftime('%Y-%m-%d')
                })

        # Running the fetch review for next batches
        for i in range(itr):
            print("==> Fetching review for batch "+str(i+2))
            result, continuation_token = reviews(
                app_id,
                continuation_token=continuation_token
            )

            for review in result:
                if review['replyContent']==None:

                        firstName = review['userName']
                        nameArr=str.split(review['userName'])
                        if len(nameArr)>1:
                            firstName = nameArr[0]

                        reviews_list.append({
                        'reviewId':review['reviewId'],
                        'user': review['userName'],
                        'firstName':firstName,
                        'rating': review['score'],
                        'content': review['content'],
                        'date': review['at'].strftime('%Y-%m-%d')
                    })       
        
        return reviews_list

    except Exception as e:
        print(f"^^^ An error occurred: {e}\n")
        return []

if __name__ == "__main__":

    with open(configManager.DUMPED_REVIEWS_JSON_FILE, 'r', encoding='utf-8') as json_file:
        reviews = json.load(json_file)
    
    if reviews:
        count = 0
        for idx, review in enumerate(reviews, 1):
            if review['isReplied']==True:
                continue
            if review['rating']!=1:
                continue
            
            reviewContent = review['content']
            skipperKeywordFound=False
            for skipperKeyword in configManager.SKIPPER_KEYWORDS:
                if skipperKeyword.lower() in reviewContent.lower():
                    print(f"==> SKIPPING Review: [{reviewContent}] as Keyword: [{skipperKeyword}] is blacklisted.\n")
                    skipperKeywordFound=True
                    break
            if skipperKeywordFound==True:
                continue        

            if count>50:
                print("==> Finished with all batches\n")
                break
            count = count + 1
            
            print(f"==> [NOT REPLIED] Review ID: {review['reviewId']} Review: [{review['content']}] UserName: [{review['user']}] FirstName: [{review['firstName']}] Rating: [{review['rating']}] Date: [{review['date']}]\n")

            agentReply=generate_reply(review['content'],review['firstName'],review['rating'])
            if agentReply=="":
                print(f"^^^ Some issue in agent reply\n")
                continue
            print(f"[AGENT]: [{agentReply}] WordCount: [{len(agentReply)}]\n")
            
            if len(agentReply)<350:
                
                user_input = 1
                if configManager.IS_AUTO_PILOT_MODE_ON==False:
                    user_input = input("@@@ Press 1 to post this reply: ")
                if user_input=="1":
                    
                    print("==> Going to post this reply")
                    resp = post_reply(review['reviewId'],agentReply)
                    
                    if resp==1:
                        review['isReplied']=True
                        review['agentReply']=agentReply
                        with open(configManager.DUMPED_REVIEWS_JSON_FILE, 'w', encoding='utf-8') as json_file:
                            json.dump(reviews, json_file, ensure_ascii=False, indent=4)
                else:
                    print("==> Skipping this review\n")
                    continue
            else:
                while True:
                    diffCount = len(agentReply) - 350
                    agentReply=trim_reply(agentReply,diffCount)
                    if agentReply=="":
                        print(f"^^^ Some issue in agent reply\n")
                        continue
                    print(f"==> [TRIMMED AGENT]: [{agentReply}] WordCount: [{len(agentReply)}]\n")
                    if len(agentReply)<350:
                        user_input = 1
                        if configManager.IS_AUTO_PILOT_MODE_ON==False:
                            user_input = input("@@@ Press 1 to post this trimmed reply: ")
                        if user_input=="1":
                            print("==> Going to post this trimmed reply")
                            resp = post_reply(review['reviewId'],agentReply)
                            if resp==1:
                                # Write the updated data back to a new file
                                review['isReplied']=True
                                review['agentReply']=agentReply
                                with open(configManager.DUMPED_REVIEWS_JSON_FILE, 'w', encoding='utf-8') as json_file:
                                    json.dump(reviews, json_file, ensure_ascii=False, indent=4)
                            break
                        else:
                            print("==> Skipping this review\n")
                            break
    else:
        print("==> No reviews found.\n")
