
import discord
import os
from discord.ext import commands
import aiohttp
import matplotlib.pyplot as plt
import io

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
    help_message.add_field(name="!language <repository_url>", value="Fetches the languages used in a GitHub repository and displays them in an embed graphically.", inline=False)
    await ctx.send(embed=help_message)

#Total of 7 commands
@bot.command() # !track command
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

@bot.command() #!contributors command
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



@bot.command() #!language command
async def language(ctx, repository_url):
    await ctx.send("Fetching lanagues for the repository...")
    split_url = repository_url.split('/')

    owner = split_url[3]
    repo_name = split_url[4]

    api_url_lang = f"https://api.github.com/repos/{owner}/{repo_name}/languages"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url_lang) as response:
            data = await response.json()

            if response.status == 404:
                await ctx.send("Repository not found, please check the URL and try again.")
                return

            elif response.status != 200:
                await ctx.send(f"Failed to fetch languages, staus code: {response.status}")
                return
            
            elif not data:
                await ctx.send("No languages found for this repository.")
                return

            languages = list(data.keys())
            bytes_count = list(data.values())
            sorted_data = sorted(data.items(), key=lambda item: item[1])

            languages = [item[0] for item in sorted_data]
            bytes_count = [item[1] for item in sorted_data]
            total_bytes = sum(bytes_count)
            percentages = [(b / total_bytes) * 100 for b in bytes_count]

            plt.figure(figsize=(9, max(4, len(languages) * 0.5)))
            bars = plt.barh(languages, percentages)
            plt.xlabel("Percentage of Code (%)")
            plt.title(f"Languages for repository {owner}/{repo_name}")

            for bar, percentage in zip(bars, percentages):
                plt.text(
                    bar.get_width() + 0.3,
                    bar.get_y() + bar.get_height() / 2,
                    f"{percentage:.1f}%",
                    va="center"
                )

            plt.xlim(0, max(percentages) * 1.2)
            plt.tight_layout()

            image_buffer = io.BytesIO()
            plt.savefig(image_buffer, format='png', bbox_inches='tight')
            plt.close()
            image_buffer.seek(0)

            chart_file = discord.File(fp=image_buffer, filename='languages_chart.png')

            lang_embed = discord.Embed(
                title=f"Languages for repository {owner}/{repo_name}",
                description="List of languages used in the repository:",
                color=discord.Color.from_rgb(255, 225, 225),
            )

            for language, bytes_count in data.items():
                lang_embed.add_field(
                    name=language,
                    value=f"{bytes_count} bytes",
                    inline=True
                )

            lang_embed.set_image(url="attachment://languages_chart.png")

            await ctx.send(embed=lang_embed, file=chart_file)

class repCheck(discord.ui.View):
    def __init__(self, repositories, repository_name):
        super().__init__(timeout=100)
        self.repositories = repositories
        self.repository_name = repository_name
        self.current_page = 0
        self.per_page = 5

    def create_embed(self):
        start_index = self.current_page * self.per_page
        end_index = start_index + self.per_page

        page_results = self.repositories[start_index:end_index]

        repo_embed = discord.Embed(
            title=f"Repositories matching '{self.repository_name}'",
            description=f"Page {self.current_page + 1}",
            color=discord.Color.from_rgb(255, 225, 225)
        )

        repo_embed.add_field(
            name="Repository Name",
            value="\n".join([f"[{repo['name']}]({repo['html_url']})" for repo in page_results]),
            inline=True
        )

        repo_embed.add_field(
            name="Owner",
            value="\n".join([repo['owner']['login'] for repo in page_results]),
            inline=True
        )

        return repo_embed


    @discord.ui.button(label="Next ➡", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction, button):
        if (self.current_page + 1) * self.per_page >= len(self.repositories):
            await interaction.response.send_message(
                "There are no more results.",
                ephemeral=True
            )
            return

        self.current_page += 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )


@bot.command() #!search command
async def search(ctx, *,repository_name):
    await ctx.send(f"Searching for {repository_name}...", delete_after=5)
    api_url_name = f"https://api.github.com/search/repositories?q={repository_name}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url_name) as response:
            data = await response.json()

            if response.status == 404:
                await ctx.send("Repository not found. Please check the name and try again.")
                return
            elif response.status != 200:
                await ctx.send(f"Failed to search for repository. Status code: {response.status}")
                return
            elif not data.get('items'):
                await ctx.send("No repositories found with that name.")
                return

            repositories = data['items']

            view = repCheck(repositories, repository_name)
            await ctx.send(embed=view.create_embed(), view=view)


@bot.command() #!user command
async def user(ctx, user__):
    await ctx.send("Fetching information for user ", delete_after=5)
    if user__.startswith("https://github.com"):
        user__ = user__.split('/')[-1]
    elif user__.startswith("http://github.com"):
        user__ = user__.split('/')[-1]
    elif user__.startswith("github.com"):
        user__ = user__.split('/')[-1]

    api_url_user = f"https://api.github.com/users/{user__}"
    async with aiohttp.ClientSession() as session:
        fetch_user = await session.get(api_url_user)
        data = await fetch_user.json()

        if fetch_user.status == 404:
            await ctx.send("User not found. Please check the username and try again.")
            return
        elif fetch_user.status != 200:
            await ctx.send(f"Failed to fetch user information. Status code: {fetch_user.status}")
            return
        elif not data:
            await ctx.send("No information found for this user.")
            return

        user_embed = discord.Embed(
            title=data['login'],
            description=data['bio'] or "No bio provided.",
            color=discord.Color.from_rgb(255, 225, 225),
        )

        user_embed.add_field(name="Name", value=data['name'] or "No name provided.", inline=True)
        user_embed.add_field(name="Public Repositories", value=data['public_repos'], inline=True)
        user_embed.add_field(name="Followers", value=data['followers'], inline=True)
        user_embed.add_field(name="Following", value=data['following'], inline=True)

        user_embed.add_field(name="Location", value=data['location'] or "No location provided.", inline=True)
        user_embed.add_field(name="Company", value=data['company'] or "No company provided.", inline=True)
        user_embed.add_field(name="Blog", value=data['blog'] or "No blog provided.", inline=True)
        user_embed.add_field(name="contributions", value=data['html_url'], inline=True)

        await ctx.send(embed=user_embed)



@bot.command() #!commits command
async def commits(ctx, repository_url):
    await ctx.send("Fetching commits for the repository...", delete_after=5)

    commit_url  = repository_url.replace(
        "github.com",
        "api.github.com/repos"
    ) + "/commits"

    async with aiohttp.ClientSession() as session:
        async with session.get(commit_url) as response:
            data = await response.json()

            if response.status == 404:
                await ctx.send("Repository not found. Please check the URL and try again.")
                return
            elif response.status != 200:
                await ctx.send(f"Failed to fetch commits. Status code: {response.status}")
                return
            elif not data:
                await ctx.send("No commits found for this repository.")
                return

            commits_embed = discord.Embed(
                title=f"Latest Commits for {repository_url}",
                description="List of latest commits:",
                color=discord.Color.from_rgb(255, 225, 225),
            )

            commits = data[:10]

            for commit in commits:
                commits_embed.add_field(
                    name="Commit Message",
                    value=f"[{commit['commit']['message'][:150]}]({commit['html_url']})",
                    inline=False
                )

            commits_embed.set_footer(text="Note: Only the latest 10 commits are displayed.")
            await ctx.send(embed=commits_embed)

@bot.command() #!issues command
async def issues(ctx, repository_url):
    await ctx.send("Fetching issues for the repository...", delete_after=5)

    issues_url = repository_url.replace(
        "github.com",
        "api.github.com/repos"
    ) + "/issues"

    async with aiohttp.ClientSession() as session:
        async with session.get(issues_url) as response:
            data = await response.json()

            if response.status == 404:
                await ctx.send("Repository not found. Please check the URL and try again.")
                return
            elif response.status != 200:
                await ctx.send(f"Failed to fetch issues. Status code: {response.status}")
                return
            elif not data:
                await ctx.send("No issues found for this repository.")
                return

            issues_embed = discord.Embed(
                title=f"Latest Issues for {repository_url}",
                description="List of latest issues:",
                color=discord.Color.from_rgb(255, 225, 225),
            )

            issues_embed.add_field(
                name="Issue Title",
                value="\n".join([f"[{issue['title']}]({issue['html_url']})" for issue in data[:10]]),
                inline=False

            )

            issues_embed.set_footer(text="Displays only 10 for now")

            await ctx.send(embed=issues_embed)

            
bot.run(os.environ.get('BOT_TOKEN'))