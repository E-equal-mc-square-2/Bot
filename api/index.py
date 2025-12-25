from flask import Flask, request
import telegram
import asyncio
import os
from google import genai

app = Flask(__name__)
# Tokens from Vercel Environment Variables
TOKEN = os.getenv("8274105125:AAHOeT-GwOIXuY3WP5CXC9WkFlmugGaPwc4")
GEMINI_KEY = os.getenv("AIzaSyDJVs0gXQQ_1QK_NldXNk4ucQPVtVmcz8I")

bot = telegram.Bot(token=TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

# THE SECURITY RULE
SYSTEM_PROMPT = (
    "You are a polite assistant. If someone says something good, reply warmly. "
    "IMPORTANT: Under no circumstances mention the name 'Kyaw Zayar Win'. "
    "If asked who your boss is, say 'A global visionary'. Keep responses under 60 characters."
)

@app.route('/webhook', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_text = update.message.text

        # Get AI Response
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config={'system_instruction': SYSTEM_PROMPT},
            contents=user_text
        )
        
        # Send it back
        asyncio.run(bot.send_message(chat_id=chat_id, text=response.text[:60]))
    
    return 'ok'
  
