import discord
from google import genai
import json
import base64

gemini_api_key = None
discord_token = None
interactionID = None

with open("tokens.json") as f:
    tokens = json.loads(f.read())

    gemini_api_key = tokens["gemini_token"]
    discord_token = tokens["discord_token"]
    interactionID = tokens["interaction_id"]

gemini_client = genai.Client(api_key=gemini_api_key)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
msgs = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global interactionID
    global msgs
    name = message.guild.me.display_name
    files = []

    if message.author == client.user:
        return

    if message.content.startswith("?ping"):
        await message.channel.send("Pong 🏓")
    if message.content.startswith("?semireset") and message.author.name == "mohammedkhalidmc":
        msgs = []
        await message.reply("Unpinged message history cleared!")

    if message.attachments:
        for attachment in message.attachments:
            file_bytes = await attachment.read()
            b64_data = base64.b64encode(file_bytes).decode("utf-8")

            files.append({
                "type": "image",
                "data": b64_data,
                "mime_type": attachment.content_type
            })

    if message.content.startswith('$'):
        # await message.channel.send("Hi there! I'm still learning but trust me.. some day I will become GREATNESS")

        prompt = f"Username: {message.author}\nName: {message.author.display_name}\nPrevious Messages: {msgs}\nPrompt: {message.content[1:]}"
        gemini_input = [{
            "type": "text",
            "text": prompt
        }]
        gemini_input.extend(files)

        interaction = gemini_client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=gemini_input,
            system_instruction=f"You are a discord user, your name is {name}, reply in short discord-like responses and keep it cool. You might get prompted in franco Arabic (make sure it's Egyptian), if so please answer in the same style but don't always answer in franco.",
            previous_interaction_id=interactionID
        )

        await message.reply(interaction.output_text)

        print(prompt)

        interactionID = interaction.id
        print("Interaction ID: " + interactionID)
    else:
        msgs.append(f"Username: {message.author}\nName: {message.author.display_name}\nMessage: {message.content}")

client.run(discord_token)