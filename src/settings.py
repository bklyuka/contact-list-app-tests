import os

from dotenv import load_dotenv

load_dotenv()


API_URL = os.environ.get("API_URL")
TEST_USER_EMAIL = os.environ.get("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD")
