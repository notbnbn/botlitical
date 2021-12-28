from discord.ext import commands
import yaml

data = {}

with open("src/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)

bot = commands.Bot(command_prefix='Im')

bot.load_extension("cogs.senatecogs")

bot.run(data.get("token"))