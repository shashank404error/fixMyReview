import requests
import json
import configManager 

def get_ollama_response(prompt, model=configManager.OLLAMA_MODEL, host=configManager.OLLAMA_API_URL):
    try:
        url = f"{host}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        responses = []
        for line in response.text.splitlines():
            if line.strip():  
                responses.append(json.loads(line))

        return responses

    except json.JSONDecodeError as e:
            print(f"^^^ JSON decoding error: {e}")
            print("^^^ Raw response:", response.text)
    except requests.RequestException as e:
            print(f"^^^ HTTP error: {e}")
    except Exception as e:
            print(f"^^^ An error occurred: {e}")

    return []

def generate_reply(review,name,appRating):

    prompt_text = f"Be my playstore review assistant. Write a polite and empathetic response strictly under 350 characters to the review for our app 'Craveo': '{review}'. Include the name, {name}, for personalization. Add an email contact (hello@craveo.co.in) for further assistance. If the review mentions a waiting list and the rating is poor you must add 'Drop us a DM on Instagram (@craveohq) to get beta access!' Must make sure the reply is within 330 characters."

    responses = get_ollama_response(prompt_text)

    final_reply=""
    if responses:
        for response in responses:
            final_reply = final_reply + response['response']
    else:
        print("^^^ No valid responses received.")
    return unicode_escape(get_substring_between_quotes(final_reply))

def trim_reply(review,diffCharacterCount):

    prompt_text = f"Be my playstore review assistant. Trim {diffCharacterCount-1} characters from the below review and make it concise without changing the meaning. 'Review': '{review}'"

    responses = get_ollama_response(prompt_text)

    final_reply=""
    if responses:
        for response in responses:
            final_reply = final_reply + response['response']
    else:
        print("^^^ No valid responses received.")
    return unicode_escape(get_substring_between_quotes(final_reply))


def get_substring_between_quotes(reply):
    start_index = reply.find('"') + 1
    end_index = reply.find('"', start_index)

    if start_index > 0 and end_index > 0:  
        substring = reply[start_index:end_index]
        return substring
    else:
        return ""

def unicode_escape(reply):
    # return reply.encode('utf-8').decode('unicode_escape')
    return reply