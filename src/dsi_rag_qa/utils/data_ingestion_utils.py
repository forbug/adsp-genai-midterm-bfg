import re
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader

BASE_URL = "https://datascience.uchicago.edu/education/masters-programs/ms-in-applied-data-science/"


def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.text
    text = re.split(r"DSI\n+\t+Data Science Institute", text)[0].strip() # remove the DSI footer

    # Remove irrelevant text
    text = re.sub(r"(?i)Skip to Main Content", "", text) 

    # Remove excessive whitespace
    text = re.sub(r"\n\n+", "\n\n", text)

    return text

def create_url_loader(extractor_function=bs4_extractor) -> RecursiveUrlLoader:
    """
    Create a RecursiveUrlLoader with the specified base URL and extractor.
    """

    # Create the RecursiveUrlLoader with the BeautifulSoup extractor
    loader = RecursiveUrlLoader(
        BASE_URL,
        use_async=True,
        max_depth=5,
        extractor=extractor_function
    )
    
    return loader

async def load_docs_from_url(url: str = BASE_URL):
    """
    Load documents from the specified URL using the RecursiveUrlLoader.
    """
    loader = create_url_loader()
    docs = loader.load()
    
    # Display the first 1000 characters of the first document
    print(f"Loaded {len(docs)} documents from {url}")
    
    return docs