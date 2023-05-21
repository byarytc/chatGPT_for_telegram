from telethon import TelegramClient, events
import openai
import logging
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']
openai.api_key = config['openai']['openai_api_key']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Send a message to ChatGPT
client = TelegramClient('session_read', api_id, api_hash)
conversation_history = []


@client.on(events.NewMessage)
async def my_event_handler(event):
    try:
        logging.info(f"Received message from {event.message.from_id.user_id}: {event.message.message}")
        conversation_history.append({"role": "user", "content": event.message.message})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        response = completion.choices[0].message.content
        logging.info(f"Sending response to {event.message.from_id.user_id}: {response}")
        await event.respond(response)
        conversation_history.append({"role": "system", "content": completion.choices[0].message.content})
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        await event.respond("Sorry, something went wrong.")

client.start()
client.run_until_disconnected()
