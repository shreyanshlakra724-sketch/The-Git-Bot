
import discord
import os
from discord.ext import commands
import aiohttp


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
    if ctx.message.content.strip().lower() != "!help":
        return
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
@bot.command()
async def track(ctx, repository_url):
    await ctx.send(f"Tracking repository...")
    split_url = repository_url.split('/')

    owner = split_url[3]
    repo_name = split_url[4]

    await ctx.send(f"Owner: {owner}, Repository Name: {repo_name}")

    api_url = repository_url.replace(
        "github.com",
        "api.github.com/repos"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()

            if response.status == 404:
                await ctx.send("Repository not found. Please check the URL and try again.")
                return

            elif response.status != 200:
                await ctx.send(f"Failed to fetch repository information. Status code: {response.status}")
                return

            repo_embed = discord.Embed(
                title = data['name'],
                description = data['description'] or "No description provided.",
                color = discord.Color.from_rgb(255, 225, 225),
                url = data['html_url']

            )

            repo_embed.add_field(name="Owner", value=data['owner']['login'], inline=True)
            repo_embed.add_field(name="Stars", value=data['stargazers_count'], inline=True)
            repo_embed.add_field(name="Forks", value=data['forks_count'], inline=True)
            repo_embed.add_field(name="Language", value=data['language'] or "No language specified", inline=True)
            repo_embed.add_field(name="License", value=data['license']['name'] if data['license'] else 'No license', inline=True)
            repo_embed.add_field(name="Template", value=data['is_template'], inline=True)
            repo_embed.add_field(name="Open Issues", value=data['open_issues_count'], inline=True)
            repo_embed.add_field(name="Watchers", value=data['watchers_count'], inline=True)
            repo_embed.add_field(name="Default Branch", value=data['default_branch'], inline=True)
            repo_embed.add_field(name="Created At", value=data['created_at'], inline=True)
            repo_embed.add_field(name="Updated At", value=data['updated_at'], inline=True)
            repo_embed.add_field(name="Owner Profile", value=data['owner']['html_url'], inline=True)
            repo_embed.set_footer(text="For more information on contributors(!contributors <repository_url>) and languages(!languages <repository_url>).")

            await ctx.send(embed=repo_embed)

@bot.command()
async def contributors(ctx, repository_url):
    await ctx.send(f"Fetching contributors for the repository...")
    split_url = repository_url.split('/')

    owner = split_url[3]
    repo_name = split_url[4]

    api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contributors"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()

            if response.status == 404:
                await ctx.send("Repository not found. Please check the URL and try again.")
                return

            elif response.status != 200:
                await ctx.send(f"Failed to fetch contributors. Status code: {response.status}")
                return

            if not data:
                await ctx.send("No contributors found for this repository.")
                return

            contributors_embed = discord.Embed(
                title=f"Contributors for {owner}/{repo_name}",
                description="List of contributors:",
                color=discord.Color.from_rgb(255, 225, 225),
            )

            for contributor in data[:25]:
                contributors_embed.add_field(
                    name=contributor['login'],
                    value=f"[Profile]({contributor['html_url']})",
                    inline=True
                )

            await ctx.send(embed=contributors_embed)


bot.run(os.environ.get('BOT_TOKEN'))