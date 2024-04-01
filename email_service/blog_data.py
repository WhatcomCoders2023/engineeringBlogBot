from dataclasses import dataclass

@dataclass
class BlogData:
    blog_title: str #from email subject
    tagline: str #short description
    description: str #from email body
    author: str #from blog name
    url: str #from  url
    image_url: str #if image is present

    def __repr__(self) -> str:
        return f'blog_title:{self.blog_title} - tagline:{self.tagline} - description:{self.description} - author:{self.author} - url:{self.url} - image_url:{self.image_url}'
