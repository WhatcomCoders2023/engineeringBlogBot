from abc import ABC, abstractmethod
from typing import List, Dict
from email_service.blog_data import BlogData

class EmailContentParserInterface(ABC):
    @abstractmethod
    def parse(self, email: str) -> BlogData:
        pass