import googleapiclient.discovery

from datetime import datetime
from googleapiclient.errors import HttpError
from typing import List

class EmailFetcher:
    def __init__(self, gmail_client: googleapiclient.discovery.Resource):
        self.gmail_client = gmail_client

    def fetch_email_from(self, sender_email: str, since_date: datetime) -> List[str]:
        query = f'from:{sender_email} after:{since_date.date().isoformat()}'
        print("query", query)
        messages = self.search_email(query)
        # print("messages", messages)
        
        all_emails_content = []
        for msg in messages:
            txt = self.gmail_client.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            all_emails_content.append(txt)
        return all_emails_content

    def search_email(self, query: str):
        try:
            # Call the Gmail API
            result = self.gmail_client.users().messages().list(userId='me', q=query).execute()
            messages = []
            if 'messages' in result:
                messages.extend(result['messages'])
            while 'nextPageToken' in result:
                page_token = result['nextPageToken']
                result = self.gmail_client.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
                if 'messages' in result:
                    messages.extend(result['messages'])
            return messages

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
