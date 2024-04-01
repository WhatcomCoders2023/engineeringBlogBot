from google.cloud import firestore
from datetime import datetime
from typing import Optional

class FirestoreWrapper:
    def __init__(self, 
                 project_id: str,
                 collection_name="engineering_blogs", 
                 database="github-commit-data"):
        self.db = firestore.Client(project=project_id, database=database)
        self.collection_name = collection_name
    
    def fetch_blog_last_timestamp(self, document_id: str) -> Optional[datetime]:
        # Document_id is just the blog name
        doc_ref = self.db.collection(self.collection_name).document(document_id)
        try:
            doc = doc_ref.get()
            if doc.exists:
                doc_data = doc.to_dict()
                if 'last_timestamp' in doc_data:
                    print(f'{document_id}: {doc_data["last_timestamp"]}')
                    return doc_data["last_timestamp"]
                else:
                    print(f'The attribute "{document_id}" does not exist in this document.')
                    return None
            else:
                print('No such document!')
                return None
        except Exception as e:
            print(f'Error: {e} No such document!')
            return None
        
    def fetch_blog_image_url(self, document_id: str) -> Optional[str]:
        doc_ref = self.db.collection(self.collection_name).document(document_id)
        try:
            doc = doc_ref.get()
            if doc.exists:
                doc_data = doc.to_dict()
                if 'image_url' in doc_data:
                    print(f'{document_id}: {doc_data["image_url"]}')
                    return doc_data["image_url"]
                else:
                    print(f'The attribute "image_url" does not exist in this document.')
                    return None
            else:
                print('No such document!')
                return None
        except Exception as e:
            print(f'Error: {e} No such document!')
            return None

    def update_last_timestamp(self, document_id: str, new_timestamp: datetime):
        """Updates the last timestamp in Datastore."""
        doc_ref = self.db.collection(self.collection_name).document(document_id)
        try:
            # Update the specified attribute
            doc_ref.update({'last_timestamp': new_timestamp})
            print(f'Successfully updated attribute last_timestamp with new value "{new_timestamp}" in document "{document_id}".')
        except Exception as e:
            print(f'An error occurred: {e}')

    # for database class
    def convert_timestamp_from_zulu_to_UTC_format(self, zulu_iso_string:str) -> datetime:
        iso_string = zulu_iso_string.replace('Z', '+00:00')
        return datetime.fromisoformat(iso_string)