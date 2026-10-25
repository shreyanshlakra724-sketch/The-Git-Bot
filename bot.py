
import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True



bot = commands.Bot(command_prefix='!', intents=intents,help_command=None)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    init_message = discord.Embed(
        title = "Github Repository Tracker",
        description = "Welcome to the Github Repository Tracker! An open-source bot allowing you to track repositories,search for repositories and many more features.To learn more type !help",
        color = discord.Color.from_rgb(255, 225, 225),
        url = "https://github.com/shreyanshlakra724-sketch/The-Git-Bot",
        type = "rich"
    )

    msg = message.content.strip().lower()

    if msg == "git init":
        await message.channel.send(embed=init_message)

    await bot.process_commands(message)

@bot.command()
async def help(ctx):
    help_message = discord.Embed(
        title = "Commands List",
        description = "All available commands:",
        color = discord.Color.from_rgb(255, 225, 225),

    )
    help_message.add_field(name="!help", value="Displays this help message.", inline=False)
    help_message.add_field(name="!track <repository_url>", value="Tracks a GitHub repository, provides all information in an embed.", inline=False)
    help_message.add_field(name="!search <repository_name>", value="Searches for a GitHub repository by name and provides information in an embed.", inline=False)
    help_message.add_field(name="!user <username>/<user_profile_link>", value="Fetches information about a GitHub user and displays it in an embed.", inline=False)
    help_message.add_field(name="!commits <repository_url>", value="Fetches the latest commits of a GitHub repository and displays them in an embed.", inline=False)
    help_message.add_field(name="!issues <repository_url>", value="Fetches the latest issues of a GitHub repository and displays them in an embed.", inline=False)
    help_message.add_field(name="!contributors <contributors>", value="Fetches the contributors of a GitHub repository and displays their profile links in an embed.", inline=False)
    help_message.add_field(name="!stats <repository_url>", value="Fetches the statistics of a GitHub repository and displays them in an embed graphically.", inline=False)
    await ctx.send(embed=help_message)

#Main Bot Commands(Total there are 6 currently might add some later)

bot.run(os.environ.get('BOT_TOKEN'))