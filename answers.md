# Part 2 — Written Answers

## 2.1 Using an LLM

**1. Where exactly in the script would you call the LLM? Describe what would change in the code.**
I would probably create a gemini file and use it instead to classify_messages logc. just put the message into a string and give it to gemini.

**2. Write an example prompt you would send to the model to classify a single message.**
"Classify the following user message into exactly one of these categories: 'grant_search', 'report_request', 'general_question', or 'unknown'. 
Reply strictly with the category name and nothing else. Remember, only use one and only one category name and don't type anything else like you understood or something like that. Exactly type like this:
Message: '{message_text}'"

**3. What response format would you expect from the model and why?**
I would expect JSON, sometning like: {"category": "grant_search"} to prevent the issues if the ai adds unnecessary text.

**4. How would you compare the quality of rule-based vs. LLM classification? What metrics would you use?**
I honestly think if implemented correctly, the rule based would be better than the LLM since the categories are very specific and clear. I would this about the accuracy of correctly categorized stuff and if the the rule-based or LLM one skipped any message or not.

**5. What risks or problems might arise from using an LLM for this task? Name at least three.**
There is too much delay as API calls are significantly slower. And AIs cost money. and also the AI might give an unwanted type of answer, break the structure, etc.

## 2.2 Extending to a Chatbot

**1. How would you store conversation history in Postgres/MySQL? Describe the table schema.**
I would probably make one table for conversations and one for messages. Conversations table would just keep stuff like id, user_id, created_at etc. Then the messages table would have id, conversation_id, message text, created_at.

**2. How would the bot "remember" previous messages when responding to a new one? Specifically: what exactly would you pass to the LLM on each request?**
I would get the previous messages from the database for that conversation_id and send them together with the new message to the AI. Something like user message, assistant response, user message etc in order. 

**3. What happens when the history gets too long for the model's context window? What options do you have?**
If the conversation gets too long, the AI can no longer fit all the messages into the context window. So I would probably either only keep the latest messages or summarize the older parts and send the summary instead. I would probably make AI also do the summary.

## 2.3 RAG for Document Search

**1. How would you prepare these PDFs for search? Describe the steps — what is chunking and why it's needed, what chunk size you'd choose and why.**
First I would extract the text from the PDFs. Then I would split the text into smaller chunks because sending entire PDFs is too large and also harder for embeddings to work correctly with. Chunking basically means dividing the text into smaller parts. I would probably use around 1000 token chunks to get a good balance chunk size.

**2. What are embeddings in this context, and where would you store them?**
Embeddings are basically lists of numbers created from the text so the system can compare meanings instead of exact words. I would store them in MySQL together with the related text chunk and document information.

**3. Describe the full flow of processing one user query — from their question to the bot's answer.**
The user asks a question. Then the system converts the question into an embedding and searches for the most similar chunks in the database. After finding the relevant chunks, it sends them together with the user question to the AI. Then the AI generates the final answer based on that context.

**4. What is the main problem that can occur if you simply concatenate the top-N retrieved chunks and send them to the LLM? How would you address it?**
Some chunks might not be relevant and can confuse the AI. Also if there is too much text, the important information can get ignored. I would try to filter the chunks first before sending them and only include the most relevant ones.
