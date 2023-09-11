import os
from services.brawlstars.services.club_service import ClubService
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
        _club_service = ClubService()

        print('test')
        members = _club_service.get_all_members_dict_by_id(os.environ['CLUB_TAG'])
        print(members)
