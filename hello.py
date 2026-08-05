from anthropic import Anthropic
from anthropic.types.text_block import TextBlock
from config import settings


client = Anthropic(api_key=settings.anthropic_api_key)

message = client.messages.create(
    model=settings.model,
    max_tokens=settings.max_tokens,
    messages=[{
        "role": "user",
        "content": "Hello, Claude"
    }]
)

print(f"Input tokens: {message.usage.input_tokens} Output tokens: {message.usage.output_tokens}")
input_price = settings.input_price_per_mtok * message.usage.input_tokens
output_price = settings.output_price_per_mtok * message.usage.output_tokens
print(f"Input price: {input_price} Output price: {output_price}")

print('. '.join([content.text for content in message.content if isinstance(content, TextBlock)]))
