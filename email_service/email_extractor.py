from typing import List
from email_service.blog_data import BlogData
from email_service.summarizer import Summarizer
from email_service.email_parser.parser_factory import ParserFactory

class EmailContentExtractor:
    def __init__(self, firestore_wrapper, 
                 parser_factory: ParserFactory):
        self.firestore_wrapper = firestore_wrapper
        self.parser_factory = parser_factory

    def extract(self, blog_name: str, emails: List[str], image_url: str) -> List[BlogData]:
        blog_data_from_emails = []
        email_parser = self.parser_factory.get_parser(blog_name, image_url)
        for email in emails:
            try:
                blog_data = email_parser.parse(email)
            except Exception as e:
                print(f"Error parsing email: {blog_name}, error: {str(e)}")
                continue
            blog_data_from_emails.append(blog_data)
        
        return blog_data_from_emails