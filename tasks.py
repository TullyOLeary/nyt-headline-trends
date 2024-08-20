from formatted_lines import get_and_format_lines
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
def fetch_and_format_lines(api_key):
    # Call the function that fetches and formats the lines
    return get_and_format_lines(api_key)
