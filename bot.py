from dotenv import load_dotenv
import os
import discord
import aiohttp
from discord import app_commands
from discord.ext import commands
from datetime import datetime

# Define the bot's intents
intents = discord.Intents.default()

# Create the bot instance without the traditional command prefix
class FoxBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')
        await self.tree.sync()  # Synchronize slash commands
        print("Slash commands synced!")

# Instantiate the bot client
bot = FoxBot()

# Define a slash command
@bot.tree.command(name="hi", description="Says hello!")
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message("Hai, I am Fox-Bot, your personal foxboy companion :fox:")
    
# Define the slash command
@bot.tree.command(name="foxes", description="Random Foxes!")
async def foxes(interaction: discord.Interaction):
    try:
        FOX_URL = 'https://randomfox.ca/floof/'

        async with aiohttp.ClientSession() as session:
            async with session.get(FOX_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    await interaction.response.send_message(data['image'])
                else:
                    await interaction.response.send_message("Could not fetch fox 🦊.")
    except Exception as e:
        print(e)
        await interaction.response.send_message("An error occurred while fetching the fox 🦊.")
        
@bot.tree.command(name="blahaj", description="Random Blahaj!")
async def blahaj(interaction: discord.Interaction):
    try:
        blahaj_URL = 'https://blahaj.transgirl.dev/images/random'

        async with aiohttp.ClientSession() as session:
            async with session.get(blahaj_URL) as response:
                if response.status == 200:
                    data = await response.json()

                    # Create an embed with the Blahaj image
                    embed = discord.Embed(
                        title="Random Blahaj!",
                        color=0xFF5733
                    )
                    embed.set_image(url=data['url'])
                    embed.set_author(
                        name=interaction.client.user.name,
                        icon_url=interaction.client.user.avatar.url
                    )

                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("Could not fetch Blahaj 🦈.")
    except Exception as e:
        print(e)
        await interaction.response.send_message("An error occurred while fetching the Blahaj 🦈.")
        
# Define the slash command
@bot.tree.command(name="bonk", description="Bonk a member!")
@app_commands.describe(target="The member to bonk")
async def bonk(interaction: discord.Interaction, target: discord.Member):
    if target:
        bonker = interaction.user.name
        bot_version = 'v.1'  # Replace with your actual bot version
        current_time = datetime.now().strftime("%I:%M %p")

        embed = discord.Embed(
            title=f"**{bonker} bonked {target.name}!**",
            color=0xFF5733  # Orange color
        )
        embed.set_author(
            name=interaction.client.user.name,
            icon_url=interaction.client.user.avatar.url
        )
        embed.set_image(url='https://media.tenor.com/oHjfWJorYB8AAAAC/bonk.gif')  # URL to the bonk GIF
        embed.set_footer(text=f"Fox-Bot Version: {bot_version} | Current Time: {current_time}")

        await interaction.response.send_message(embed=embed)
        
        
load_dotenv()  # Load environment variables from .env file

bot_token = os.getenv('DISCORD_BOT_TOKEN')

# Run the bot with your token
bot.run(bot_token)
