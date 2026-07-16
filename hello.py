import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.environ.get("API_KEY"))

messages = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Hello, Claude"
    }]
)

for message in messages:
    print(message)
