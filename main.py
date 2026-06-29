import discord
from google import genai
import json

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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global interactionID
    name = message.guild.me.display_name

    if message.author == client.user:
        return

    if message.content.startswith("?ping"):
        await message.channel.send("Pong 🏓")

    if message.content.startswith('$'):
        # await message.channel.send("Hi there! I'm still learning but trust me.. some day I will become GREATNESS")

        prompt = f"Username: {message.author}\nName: {message.author.display_name}\nPrompt: {message.content[1:]}"

        interaction = gemini_client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=prompt,
            system_instruction=f"You are a discord user, your name is {name}, reply in short discord-like responses and keep it cool. You might get prompted in franco Arabic (make sure it's Egyptian), if so please answer in the same style but don't always answer in franco.",
            previous_interaction_id=interactionID
        )

        await message.channel.send(interaction.output_text)

        print(prompt)

        interactionID = interaction.id
        print("Interaction ID: " + interactionID)

client.run(discord_token)