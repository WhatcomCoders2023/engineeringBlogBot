import os

from firestore_wrapper import FirestoreWrapper
from bot_service.bot import EngineeringBlogBot
from email_service.service import EmailService
from dotenv import load_dotenv
from constants import BLOG_NAMES
from util import access_secrets

load_dotenv()

def main(data, context):
    project_id = os.getenv('PROJECT_ID')
    bot_token = access_secrets(project_id=project_id, secret_id="engineering_blog_bot_token")
    firestore_wrapper = FirestoreWrapper(project_id=os.getenv('PROJECT_NAME'))
    email_service = EmailService(firestore_wrapper)
    all_blog_data = []
    for blog in BLOG_NAMES:
        blog_data = email_service.extract(blog)
        if blog_data:
            all_blog_data.extend(blog_data)
    
    channel_ids = [int(os.getenv("ML_CHANNEL_ID")), 
                   int(os.getenv("ENGINEERING_BLOG_CHANNEL_ID")), 
                   int(os.getenv("PRODUCT_CHANNEL_ID"))]
    bot = EngineeringBlogBot(all_blog_data, channel_ids)
    bot.run(bot_token) 

    
if __name__ == '__main__':
    main("", "")