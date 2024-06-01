from dotenv import load_dotenv
import os

load_dotenv()

def read_secret(name: str):
    value = os.getenv(name)
    if value is None:
        raise Exception(f"{name} environment variable is not found")
    return value