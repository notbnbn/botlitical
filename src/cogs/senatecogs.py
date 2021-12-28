from discord import PartialEmoji
from discord.ext import commands
import yaml

data = {}

with open("src/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)

class SenateCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        chid = data.get("senate_channel")
        guild = payload.member.guild
        channel = guild.get_channel(chid)
        role = guild.get_role(data.get("senate_role"))
        emoji = payload.emoji.name
        msg = await channel.fetch_message(payload.message_id)
        buysell = {"buynow":"<:buynow:845805676499435541>", "sellnow":"<:sellnow:845805705683271690>"}
        buynum = 0
        sellnum = 0

        for reaction in msg.reactions:
            if type(reaction.emoji) is PartialEmoji:
                if reaction.emoji.name == "buynow":
                    buynum = reaction.count
                elif reaction.emoji.name == "sellnow":
                    sellnum = reaction.count

        if payload.channel_id == chid:
            if emoji == 'buynow' or emoji == 'sellnow':
                if role not in payload.member.roles:
                    await msg.remove_reaction(payload.emoji, payload.member)
                    if(data.get("atv")):
                        await self.trg.send(":no_entry: " + payload.member.name + " tried to react with " + buysell.get(payload.emoji.name))
                else:
                    if(data.get("atv")):
                        await self.trg.send(":white_check_mark: " + payload.member.name + " reacted with " + buysell.get(payload.emoji.name) + "\n"
                                            "<:buynow:845805676499435541> **" + str(buynum) + "** | **" + str(sellnum) + "** <:sellnow:845805705683271690>")
                    
    @commands.Cog.listener()
    async def on_ready(self):
        if data.get("atv"):
            self.trg = await self.bot.fetch_user(data.get("trg"))
        print('Ready :)')

def setup(bot):
    bot.add_cog(SenateCogs(bot))