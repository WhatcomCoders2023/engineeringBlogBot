from email_service.blog_data import BlogData
from discord import Embed
from discord.ext import commands
from typing import List 
from constants import BLOG_NAME_TO_CHANNEL

class EmailCog(commands.Cog):
    def __init__(self, bot, all_blog_data: List[BlogData], channel_ids: List[int]):
        self.bot = bot
        self.all_blog_data = all_blog_data
        self.channel_ids = channel_ids

    async def send_blog_postings(self, channel, blog_data):
        await channel.send('🚀 **Loading new blog posts...** 🚀')

        # for blog_data in self.all_blog_data:
        # Enhanced Embed Layout
        embed = Embed(
            title=blog_data.blog_title, 
            url=blog_data.url,  # Makes the title clickable
            description=blog_data.tagline,  # Keep it short and engaging
            color=0x1A1A1A)  # A sleek, dark theme color
            
        # Adding author and URL in a more compact way
        embed.set_author(name=f"By {blog_data.author}", icon_url=blog_data.image_url)
        
        if blog_data.image_url:
            embed.set_image(url=blog_data.image_url)
        
        # Adding a "Read more" button-like text, assuming you have a valid URL.
        if blog_data.url:
            embed.add_field(name="Explore", value=f"[Read More ➜]({blog_data.url})", inline=True)
        
        # Description can be long, so it's not in the initial embed to keep it clean
        message = await channel.send(embed=embed)
        
        # Create a thread for detailed discussion, including the long description.
        thread_name = f"Discussion: {blog_data.blog_title[:87]}"  # Limit thread name to 100 chars
        thread = await message.create_thread(name=thread_name, auto_archive_duration=1440)  # 1 day
        await thread.send(f"**Let's discuss!**\n\n{blog_data.description[:1900]}...") # Limit to 2000 chars

    @commands.Cog.listener()
    async def on_ready(self):
        print('Engineering blog post Cog is ready!')
        for blog_data in self.all_blog_data:
            channel_type = BLOG_NAME_TO_CHANNEL.get(blog_data.author)
            if channel_type == 'engineering':
                channel_id = self.channel_ids[1]
            elif channel_type == 'ml':
                channel_id = self.channel_ids[0]
            elif channel_type == 'product':
                channel_id = self.channel_ids[2]
            try:
                if channel_id is None:
                    print(f"Channel with ID {channel_id} not found.")
            except Exception as e:
                print(e)
                continue

            channel = self.bot.get_channel(channel_id)
            print(f"Sending blog post to channel {channel_id}")
            print(channel)
            await self.send_blog_postings(channel, blog_data)
        await self.bot.close()

        