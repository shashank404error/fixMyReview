# FixMyReview AI Agent

FixMyReview is open-source AI agent which can categorize and reply to all the reviews from the Google Play Store in realtime. This eventually improve user satisfaction and helps gain actionable insights.

---

## Features

- **Real time**: Just run the agent, and it’ll keep checking for new reviews and responding to them in real-time.
- **Keyword Extraction**: Spot common themes, keywords, or issues in reviews and reply accordingly.
- **Dual Mode**: Operate on autopilot or stay in full control, your choice!
- **Multi Response**: Continuously refine replies until they meet all Play Store response guidelines.
- **Trends and Insights**: Monitor review trends over time to understand user sentiment and app performance.
- **Integration Ready**: Seamlessly integrate it into your workflows based on review categories.

---

## Prerequisites

- Python 3.8+
- Google Play Store API credentials (optional for running realtime)
- `Ollama` framework to run LLMs in your local setup

## Setup configManager.py

1. Add your `APP_PACKAGE_NAME`.
2. Set `IS_AUTO_PILOT_MODE_ON` to switch between auto-pilot or manual mode. 
3. Add any keywords to `SKIPPER_KEYWORDS` to filter out reviews containing these terms.
---
## How to use

### *Realtime (Fetches reviews only from the past 7 days)*

1. Clone the repository:
   ```bash
   git clone https://github.com/shashank404error/fixMyReview.git
   cd fixMyReview
2. Copy & paste your service-account.json file in creds.json.
3. Install all required dependencies from `requirements.txt`.
4. Download Ollama from [here](https://ollama.com/).
5. Run llama model:
    ```bash
    ollama run llama
6. Run the code:
    ```bash
    python3 fetchReviewsWithCreds.py 

### *Bulk Reviews (Fetches all publicly available reviews)*

1. Clone the repository:
   ```bash
   git clone https://github.com/shashank404error/fixMyReview.git
   cd fixMyReview
2. Install all required dependencies from `requirements.txt`.
3. Run the code:
    ```bash
    python3 web2JSON.py     
4. Download Ollama from [here](https://ollama.com/).
5. Run llama model:
    ```bash
    ollama run llama
6. Run the code:
    ```bash
    python3 fetchReviewsWithoutCreds.py 

---
## Screenshots
![App Screenshot]([https://via.placeholder.com/468x300?text=App+Screenshot+Here](https://raw.githubusercontent.com/shashank404error/fixMyReview/refs/heads/main/input/screenshot.jpg))

---
## Contributing

Contributions are always welcome!


## Author

- [@shashank404error](https://www.github.com/shashank404error)


