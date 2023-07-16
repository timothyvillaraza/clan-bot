import discord
import asyncio # USED TO CATCH TIMEOUT ERRROR RAISED BY discord.Client.wait_for()
import requests
from discord.ext import commands
from collections import defaultdict

# Setup Function
async def setup(bot):
    await bot.add_cog(WordFrequency(bot))


# Cog Class
class WordFrequency(commands.Cog):
    # Initalizer
    def __init__(self, bot):
        self.bot = bot
        self.frequencyMaps = {}  # Use database eventually, username -> FrequencyMap
    
    # Class Definitions
    class FrequencyMap:
        def __init__(self, username):
            self.username = username
            self.sfw = False # Default: True
            self.wordFreq = defaultdict(int) # defaultdict(int): Nonexistant keys assigned 0
            self.sortedKeys = None
            self.pages = []


    """
    
    Helper Functions
    
    """

    def filterMessage(self, message):
        """
        TODO: Handle Request Errors

        www.purgomalum.com

        Filters a message of profanity. Any censored words
        are replaced with '*' equal to the length of the word

        """

        URL = f'https://www.purgomalum.com/service/json'
        PARAMS = {'text': message}
        responce = requests.get(url=URL, params=PARAMS)
        data = responce.json()

        return data['result']


    def generateWordFrequency(self, author, userInput):
        """

        Take each word in the input and count up it's occurances.
        Returns the author, word frequency dictionary, and descending order keys for the word frequency.

        """

        author_wordFreq = author.wordFreq
        
        if author.sfw:
            message = self.filterMessage(userInput.casefold())
        else:
            message = userInput.casefold()

        # If a key doesn't exist, add it with a default value of 0
        for word in message.split():
            # If the current word was not censored (not all '*')
            if word != len(word) * '*':
                author_wordFreq[word] += 1

        # sorted() returns a *list* of key from most freq keys to least freq keys
        sorted_wordFreqKeys = sorted(
            author_wordFreq, key=author_wordFreq.get, reverse=True)

        return author, author_wordFreq, sorted_wordFreqKeys


    def printWordFreq(self, user):
        """

        CONSOLE ONLY

        Prints word frequency for a specific user to the console

        """

        print(f'     [Word Count for {user.name}]')
        for currentKey in user.sortedKeys:
            print(f"     {currentKey}: {user.wordFreq[currentKey]}")

        return


    def createWordFreqString(self, user):
        """

        Returns a word frequency string. Used for the discord bot reply.

        """

        word_frequency = ''
        for rank, key in enumerate(user.sortedKeys):
            word_frequency += (f"     #{rank + 1} - {key}: {user.wordFreq[key]}\n")

        return word_frequency


    def createPages(self, message, nWords=10):
        """

        Recives a word frequency string in list form and
        returns them divides into pages by 'nWords' words.

        """

        page = ''
        pages = []

        # Push every 'nWords' words into the 'pages' list
        for i, word in enumerate(message.split('\n')):
            if i % nWords == 0 and page != '':
                pages.append(page)
                page = ''

            page += word + '\n'

        # Push the remainder of words into the last page
        if page != '':
            pages.append(page)

        return pages
    
    def createEmbedMessage(self, user, userFreq, message):
        # Body of Message
        embed_message = discord.Embed(
            title='Word Count',
            color=discord.Color.blue(),
            description=message
        )

        # Appears at the top of the message
        embed_message.set_author(
            name=user.display_name,
            icon_url=user.avatar_url
        )

        return embed_message


    """

    Discord Events

    """

    # NOTE: functions decorated with @bot.listen recieves 'Message' instances
    # Listen for Messages (Recieves message object)
    # All events will be slow because this function is ran first?
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # Prevents bot from responding to itself
        if message.author == self.bot.user:
            return

        # Look up mentioned user's word frequency
        if message.author in self.frequencyMaps:
            # Existing User: Pull up from database
            mentioned_word_freq = self.frequencyMaps[message.author]
        else:
            # New User: Add to database
            mentioned_word_freq = self.FrequencyMap(message.author)
            self.frequencyMaps.update({message.author: mentioned_word_freq})

        # Create a word frequency map based on the recieved message
        word_frequency = self.generateWordFrequency(mentioned_word_freq, message.content)

        # Update the mentioned_word_freq's word frequency table
        mentioned_word_freq = word_frequency[0]
        mentioned_word_freq.wordFreq = word_frequency[1]
        mentioned_word_freq.sortedKeys = word_frequency[2]

        # DEBUG: Prints frequency map to CONSOLE
        # printWordFreq(author_freq_map)
        # print()


    # NOTE: name_of_variable : type_of_instance is a discord.py conversion feature
    # TODO: Add ability to look up nth most used word
    @commands.command()
    async def freq(self, ctx, mentioned_user: discord.Member):
        # If no mention was included in the mention, return.
        # if len(ctx.message.mentions) < 1:
        #     return

        # Look up mentioned user in database
        if mentioned_user in self.frequencyMaps:
            # Word frequency of mentioned user
            mentioned_freq = self.frequencyMaps[mentioned_user]

            # Convert their word frequency table a string
            word_frequncy_string = self.createWordFreqString(
                self.frequencyMaps[mentioned_user])

            # Paginate string and save to instance
            mentioned_freq.pages = self.createPages(word_frequncy_string)

            # Convert pages from string format into embed
            page = mentioned_freq.pages[0]

            embed_message = self.createEmbedMessage(mentioned_user, mentioned_freq, page)

            # Appears at the bottom of the message
            embed_message.set_footer(
                text=f'page 1/{len(mentioned_freq.pages)}'
            )

            # Send and store sent message as a 'message' instance
            bot_message = await ctx.send(embed=embed_message)

            # Set emoji's for arrows
            arrow_left = '⬅️'
            arrow_right = '➡️'

            # Add reactions to the send message
            await bot_message.add_reaction(arrow_left)
            await bot_message.add_reaction(arrow_right)

            # Conditions to wait for (Used down below as an arg)
            def check(reaction, user):
                # print('Checking Reaction')
                if reaction.message != bot_message:
                        return False

                return user != self.bot.user and str(reaction.emoji) in [arrow_left, arrow_right]

            current_page_index = 0

            # Change pages with arrow react
            # TODO: For every active message, any reactions to any messages will 
            #       run check() that many times causing performance issues.
            while True:
                try:
                    # Raises asyncio.TimeoutError to break out of the loop
                    # Flow of statements continue if check() returns true or if wait_for times out
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=120, check=check)

                    if str(reaction.emoji) == '➡️':
                        current_page_index = (current_page_index + 1) % len(mentioned_freq.pages)

                    elif str(reaction.emoji) == '⬅️':
                        current_page_index = (current_page_index - 1) % len(mentioned_freq.pages)

                    # Create the new message to display
                    embed_message = self.createEmbedMessage(mentioned_user, mentioned_freq, mentioned_freq.pages[current_page_index])
                    embed_message.set_footer(
                        text=f'page {current_page_index + 1}/{len(mentioned_freq.pages)}'
                    )

                    # Edit bot's discord message
                    await bot_message.edit(embed=embed_message)

                except asyncio.TimeoutError:
                    # print('Time Out')
                    break
                    # ending the loop if user doesn't react after x seconds


    # TODO: Look up type() vs isinstance()
    @freq.error
    async def freq_error(self, ctx, error):
        """

        Error Handiling for .freq

        """

        # isinstance(incoming_instance, is_instance_this_type)
        if isinstance(error, commands.MissingRequiredArgument):
            print(
                f'freq ERROR: {ctx.author} did not specify which member to look up.'
                )
