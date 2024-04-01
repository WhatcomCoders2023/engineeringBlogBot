import discord
from discord.ext import commands
from bot_service.email_cog import EmailCog
from typing import List

class EngineeringBlogBot(commands.Bot):
    def __init__(self, 
                 all_email_content: List[str], 
                 channel_id: List[int], 
                 command_prefix="!", 
                 intents=discord.Intents.all()):
        self.all_email_content = all_email_content
        self.channel_id = channel_id
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        # Load your cogs here
        await self.add_cog(EmailCog(self, self.all_email_content, self.channel_id))
        # Setup actions like sending a startup message can also go here
        print('Bot setup complete!')