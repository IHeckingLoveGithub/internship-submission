# Digi Media Assignment

## Description
This script basically loads a JSON that contains of user messages and the cleans it. Then it categorizes each message based on predetirmined categories and keywords And then the messages are saved to CSV and summary text file and also stored in the MySQL database.

> **Database Choice**: I used MySQL instead of PostgreSQL since I know MySQL and I don't really use PostgreSQL.

## Setup and Installation

1. **Install Requirements**
   Install the requirements like this:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Copy the example file and configure it:
   ```bash
   cp .env.example .env
   ```
   Then open the `.env` file and set it according to your MySQL credentials.

## Running the Script
To run the script, execute the command:
```bash
python src/main.py
```

## Decisions Made During Cleaning and Classification

**Cleaning**:
Messages and user_ids that were null or empty strings were dropped.
Whitespaces on the messages were removed.

**Classification**:
If a keyword appears anywhere in the message, it is counted.
If a message contains multiple keywords, the first one is chosen and accordingly categorized. 

## Improvements with 2-3 More Days
I would honestly just add an LLM like gemini api call to classify the messages to make them more accurate. and also do better error handling and fix the bugs.

## Time Spent
1 Hour was spent to review the assignment before the interview. and then roughly 2-3 hour was spent to do the task. Doing the answers and README took longer then I anticipated.