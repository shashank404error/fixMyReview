import json
import configManager
import fetchReviewsWithoutCreds

def fetch_app_review_and_dump_to_json():
    app_id = configManager.APP_PACKAGE_NAME
    review_count = configManager.REVIEW_COUNT_PER_BATCH_SCRAPING_MODE
    iterations = configManager.TOTAL_BATCH_SCRAPING_MODE
    reviews = fetchReviewsWithoutCreds.fetch_app_reviews(app_id, review_count,iterations)

    ## store this locally so we donot process it twice
    with open(configManager.DUMPED_REVIEWS_JSON_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(reviews, json_file, indent=4)
        print(f"==> Reviews stored to {configManager.DUMPED_REVIEWS_JSON_FILE} successfully.")

    with open(configManager.DUMPED_REVIEWS_JSON_FILE, 'r', encoding='utf-8') as json_file:
        reviews = json.load(json_file)
    
    if reviews:
        count = 0
        for idx, review in enumerate(reviews, 1):  
            review['isReplied']=False
            review['agentReply']=""
            with open(configManager.DUMPED_REVIEWS_JSON_FILE, 'w', encoding='utf-8') as json_file:
                json.dump(reviews, json_file, ensure_ascii=False, indent=4) 

    print(f"==> Review structure transformed for fixMyReview Agent.")

fetch_app_review_and_dump_to_json()