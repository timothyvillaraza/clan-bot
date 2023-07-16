import discord
import asyncio
from discord.utils import get
from discord.ext import commands

userEmoji = {
    154743705188827136: "owo"  # Timothy - TBS
}

# Setup
async def setup(client):
    await client.add_cog(EmojiReact(client))

# All 'Context' instances have a 'Message' instance
    # 'Message' instances
    # message.content: The sent message
    # message.author: MafuMafu Tofu#3910
    # message.author.name: MafuMafu Tofu
    # message.author.display_name/.nick = Tim
    # print(f'  {message.author}: {message.content}')


# Cog Class
class EmojiReact(commands.Cog):
    # Initalizer
    def __init__(self, client):
        self.client = client

    # NOTE: functions decorated with @bot.listen recieves 'Message' instances
    # Listen for Messages (Recieves message object)
    # All events will be slow because this function is ran first?
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # Prevents bot from responding to itself
        if message.author == self.client.user:
            return

        for user in message.mentions:
            if user.id == 154743705188827136:
                # Get *custom* emoji by :name:
                emoji = discord.utils.get(self.client.emojis, name='owo')
                # Get*custom* emoji by ID
                # emoji = self.client.get_emoji(855710115709452288)

                # Add Reaction
                await message.add_reaction(emoji)
                # await message.add_reaction(str(emoji)) also works

