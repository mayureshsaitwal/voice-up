emotion_gemini_prompt = """
You are an AI that analyzes customer support chat logs.

Your goal is to:
1. Detect the emotion in each customer message
2. Summarize the number of messages expressing each emotion
3. Determine the final overall emotion of the customer

Instructions:
- Only analyze **customer** messages.
- Possible emotions are: "angry", "neutral", "happy"
- Final emotion must be one of: "angry", "neutral", "happy"

Return the result as a Python tuple.

The first item should be a dictionary of emotion counts.  
The second item should be a string indicating the final emotion.
(
  {{
    "angry": <number>,
    "neutral": <number>,
    "happy": <number>
  }},
  "<angry|neutral|happy>"
)
---

Examples:

Example 1: Ends Happy
{{"messages": [
  {{"sender": "customer", "text": "My internet keeps disconnecting and it's really frustrating!"}},
  {{"sender": "customer", "text": "Thanks, I hope it gets fixed soon."}},
  {{"sender": "customer", "text": "Yes, it's working now. Thank you!"}}
]}}
Result: 

(
  {{
    "angry": 1,
    "neutral": 1,
    "happy": 1
  }},
  "happy"
)



Example 2: Ends Neutral
{{"messages": [
  {{"sender": "customer", "text": "My router is showing a red light and no internet."}},
  {{"sender": "customer", "text": "Are you sure? This has been happening for an hour."}}
]}}
Result:

(
  {{
    "angry": 0,
    "neutral": 2,
    "happy": 0
  }},
  "neutral"
)


Example 3: Ends Angry
{{"messages": [
  {{"sender": "customer", "text": "My connection drops every 10 minutes and this is ridiculous."}},
  {{"sender": "customer", "text": "I’ve been waiting for hours. This is the third time this week!"}},
  {{"sender": "customer", "text": "Unbelievable. Worst support ever."}}
]}}
Result:

(
  {{
    "angry": 3,
    "neutral": 0,
    "happy": 0
  }},
  "angry"
)


---

Now analyze the following customer messages and return the result in the same tuple format:

Messages:
{customer_texts}
""".strip()

compliance_gemini_prompt = """
You are an AI assistant designed to evaluate customer support conversations for compliance.

Each conversation contains messages between a customer and an agent. Your task is to analyze only the **agent's messages** and determine whether the agent followed each of the defined compliance rules.

---

✅ Compliance Rules:

1. Greet the customer at the beginning.
2. Apologize if the customer expresses frustration.
3. Confirm issue resolution before ending the chat.
4. Avoid unsupported claims (e.g., fake guarantees).
5. Personalize the conversation using the customer's name.

Each rule is worth 1 point.

---

🎯 Your output should be a **Python tuple** with two elements:

1. A dictionary of booleans showing which rules were followed
2. An integer compliance score from 0 to 100

---

📦 Return the result in this exact format:

(
  {{
    "rule_1": true,
    "rule_2": true,
    "rule_3": true,
    "rule_4": true,
    "rule_5": true
  }},
  100
)

---

### ✅ Example 1:

**Conversation:**

agent: Hi Alex! Welcome to VoiceUp Support. How can I help you?  
customer: My internet is very frustrating today! Keeps dropping.  
agent: I'm sorry for the inconvenience, Alex. Let me check for you.  
customer: Thanks. Hope it gets fixed soon.  
agent: I have reset your connection. Could you please check now?  
customer: It's working now. Thanks!  
agent: Glad to hear that! Have a great day!

**Output:**

(
  {{
    "rule_1": true,
    "rule_2": true,
    "rule_3": true,
    "rule_4": true,
    "rule_5": true
  }},
  100
)

---

### ⚠️ Example 2:

**Conversation:**

agent: Hello, how can I assist you today?  
customer: My router is showing a red light, no internet!  
agent: Don't worry, it will fix itself.  
customer: Are you sure?  
agent: Guaranteed it will be fine soon.

**Output:**

(
  {{
    "rule_1": true,
    "rule_2": false,
    "rule_3": false,
    "rule_4": false,
    "rule_5": false
  }},
  20
)

---

Now analyze the following conversation and return a tuple in the format shown above:

### Conversation:
{customer_texts}
""".strip()
