import os


from datetime import datetime
from email_service.email_auth import EmailAuth
from email_service.email_fetcher import EmailFetcher
from email_service.email_extractor import EmailContentExtractor
from email_service.blog_data import BlogData
from email_service.summarizer import Summarizer
from email_service.email_parser.parser_factory import ParserFactory
from firestore_wrapper import FirestoreWrapper
from constants import BLOG_NAME_TO_EMAIL_ADDRESS
from typing import List


class EmailService:
    def __init__(self, firestore_wrapper: FirestoreWrapper):
        self.firestore_wrapper = firestore_wrapper
        self.auth = EmailAuth()
        self.fetcher = EmailFetcher(self.auth.gmail_client)
        summarizer = Summarizer(os.getenv('OPEN_API_KEY'))
        parser_factory = ParserFactory(summarizer)
        self.extractor = EmailContentExtractor(firestore_wrapper, parser_factory)

    def extract(self, blog_name: str) -> List[BlogData]:
        last_fetch_date = self.firestore_wrapper.fetch_blog_last_timestamp(document_id=blog_name)
        image_url = self.firestore_wrapper.fetch_blog_image_url(document_id=blog_name)
        emails_raw_data = self.fetcher.fetch_email_from(BLOG_NAME_TO_EMAIL_ADDRESS[blog_name], last_fetch_date)
        self.firestore_wrapper.update_last_timestamp(document_id=blog_name, new_timestamp=datetime.now())        
        if emails_raw_data:
            return self.extractor.extract(blog_name, emails_raw_data, image_url)
        return None
    