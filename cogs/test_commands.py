import discord
import asyncio
from discord.ext import commands


# Setup
async def setup(client):
    await client.add_cog(TestCommands(client))


# All 'Context' instances have a 'Message' instance
    # 'Message' instances
    # message.content: The sent message
    # message.author: MafuMafu Tofu#3910
    # message.author.name: MafuMafu Tofu
    # message.author.display_name/.nick = Tim
    # print(f'  {message.author}: {message.content}')


# Cog Class
class TestCommands(commands.Cog):
    # Initalizer
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def eli(self, ctx):
        await ctx.send('Eli? She\'s only the cutest girl around!')

    # Test Mention
    @commands.command()
    async def test(self, ctx):
        test = ctx.author
        await ctx.send(f'{test}')

    # NOTE: functions decorated with @commands.command recieves 'Context' instances
    # Test Mention
    @commands.command()
    async def mention(self, ctx, mentioned_user: discord.Member):
        await ctx.send(f'{mentioned_user}')

    @commands.command()
    async def pages(self, ctx):
        contents = ["This is page 1!", "This is page 2!", "This is page 3!", "This is page 4!"]
        pages = 4
        cur_page = 1
        message = await ctx.send(f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                break
                # ending the loop if user doesn't react after x seconds
        