import os
import discord
import asyncio
import requests
from discord.ext import commands


# Setup
async def setup(client):
    await client.add_cog(ApiTestCommands(client))


# Cog Class
class ApiTestCommands(commands.Cog):
    # Initalizer
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ApiTest(self, ctx):
        # Assemble URL
        requestUrl = f"https://api.brawlstars.com/v1/clubs/{os.environ['CLUB_TAG']}"

        response = requests.get(
            requestUrl,
            headers={'Authorization': "Bearer " + os.environ['JWT_TOKEN']})

        if response.status_code == 200:
            json_response = response.json()

            members_dict = {}
            for member in json_response["members"]:
                member_tag = member["tag"]
                members_dict[member_tag] = member
        
        print(members_dict)
