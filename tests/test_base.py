from src.mpfutils.ai import OpenAIClient
from src.mpfutils.cosmosdb import CosmosDBContainer
from src.mpfutils.azstorage import AzsContainerClient
import pytest
import logging
import os

logging.basicConfig(level=logging.INFO)

@pytest.mark.skip(reason="Focusing on Azure Storage tests")
def test_openai_client():
    c = OpenAIClient()
    capital = c.run_prompt("What is the capital of France?")
    assert "Paris" in capital

@pytest.mark.skip(reason="Focusing on Azure Storage tests")
def test_cosmosdb_client():
    c = CosmosDBContainer("posts", "schedules")
    items = c.run_query("SELECT * FROM c")
    assert len(items) > 10

def test_azstorage_client():
    sas_url = os.getenv("AZSTORAGE_TEST_SAS")
    c = AzsContainerClient("mpfutils-test", sas_url=sas_url)
    url = c.upload_blob("test.txt", "This is a test")
    assert url.startswith("https://")
    data = c.download_blob("mpfutils-test", "test.txt")
    assert data == b"This is a test"