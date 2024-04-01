import traceback
from openai import OpenAI

MAX_RETRIES = 3

class Summarizer:
    def __init__(self, open_ai_key: str):
        self.openai_client = self.load_chatgpt(open_ai_key)

    def load_chatgpt(self, api_key):
        return OpenAI(api_key=api_key)
    
    def generate_summary(self, blog_title, blog_name, blog_description, email_content: str):
        prompt = (f"Summary: Provide a brief, compelling summary of the article, capturing the essence of the innovation discussed, "
                  f"the problem it aims to solve, and the potential impact on the industry. Highlight key points that set this article "
                  f"apart from conventional wisdom or practices in the field. Core Concepts and Takeaways: [Concept 1]: Describe [Concept 1] "
                  f"in a way that both novices and experts can appreciate. What makes this concept critical to understanding the article's thesis? "
                  f"[Concept 2]: Explain [Concept 2]'s role in the broader context of [Technology/Methodology/Approach], including any challenges "
                  f"or opportunities it presents. [Concept 3]: Unpack how [Concept 3] ties everything together, providing a new lens through which "
                  f"to view [Relevant Field/Application Area]. Why Read Further? Conclude with a teaser that encourages deeper exploration. What unique "
                  f"insights, detailed analyses, or groundbreaking ideas will readers uncover by delving into the full article? Emphasize the value of "
                  f"engaging with the text not just for immediate knowledge, but for sparking long-term innovation and curiosity in their own projects "
                  f"and research. The blog title is called {blog_title} which is by {blog_name}. This is about {blog_description}. Here is the content: {email_content}")
        
        attempt = 0
        while attempt < MAX_RETRIES:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": ("You are writing a compelling summary for a blog post that will be posted in a Discord server. "
                                                       "The response/summary should be less than 2000 characters. Please only return the summary. Also, "
                                                       "break it into paragraphs for readability")},
                        {"role": "user", "content": prompt}],
                )
                summary = response.choices[0].message.content
                
                # Truncate the summary if it exceeds 2000 characters
                if len(summary) > 2000:
                    summary = summary[:1997] + "..."  # Adding ellipsis to indicate truncation
                
                return summary
            
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                traceback.print_exc()  # Optional: For detailed error logging. Consider removing or logging appropriately in production.
                attempt += 1
        
        return None  # Return None if all retries fail
