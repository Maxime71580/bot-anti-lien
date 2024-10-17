import discord
import re
from discord.ext import commands
from dotenv import load_dotenv
import os

# Intents requis pour que le bot puisse lire les messages
intents = discord.Intents.default()
intents.message_content = True

# Initialisation du bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste blanche des domaines autorisés
allowed_domains = [
    "youtube.com",
    "youtu.be",
    "twitch.tv",
    "discord.com",
    "discord.gg",
    "spotify.com"
]

# Expression régulière pour détecter les liens
url_regex = re.compile(r'(https?://\S+)')


# Événement de suppression de message contenant un lien non autorisé
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ne pas réagir aux messages du bot lui-même

    # Recherche de tous les liens dans le message
    urls = url_regex.findall(message.content)

    for url in urls:
        # Si le lien n'appartient pas à un domaine autorisé, on supprime le message
        if not any(domain in url for domain in allowed_domains):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, les liens ne sont pas autorisés.")
            return  # Une fois supprimé, on arrête d'examiner les autres liens potentiels

    # Ne pas oublier de traiter les autres commandes si présentes
    await bot.process_commands(message)


load_dotenv()

token = os.getenv("TOKEN")
bot.run(token)

