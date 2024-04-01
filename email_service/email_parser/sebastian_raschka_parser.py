import base64
import html

from email_service.blog_data import BlogData
from email_service.summarizer import Summarizer
from email_service.email_parser.email_content_parser_interface import EmailContentParserInterface
from email_service.blog_data import BlogData

class SebastianRaschkaEmailParser(EmailContentParserInterface):
    def __init__(self, summarizer: Summarizer, blog_name: str, image_url: str):
        self.summarizer = summarizer
        self.blog_name = blog_name
        self.image_url = image_url

    def parse(self, email: str) -> BlogData:
        tagline = html.unescape(email['snippet']).strip()
        payload = email['payload']
        headers = payload.get('headers')
        parts = payload.get('parts')[0]
        data = parts['body']['data']
        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode(data)
        
        
        subject = None
        for header in headers:
            if header['name'] == 'List-Post':
                newsletter_url = header['value'].strip('<>')
                
            if header['name'] == 'Subject':
                subject = header['value']
                
                
        summary = self.summarizer.generate_summary(
            subject,
            self.blog_name,
            tagline,                               
            decoded_data.decode('UTF-8'))
    
        blog_data = BlogData(
                     blog_title=subject, 
                     tagline=tagline,
                     description=summary,
                     author=self.blog_name, 
                     url=newsletter_url, 
                     image_url=self.image_url)
        return blog_data