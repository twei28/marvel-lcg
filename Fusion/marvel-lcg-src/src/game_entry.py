import os
import requests
import time
from datetime import datetime
def get_current_date(url: str = 'https://itch.io') -> int:
    try:
        response = requests.head(url, timeout=3)
        response.raise_for_status()
        date_header = response.headers.get('Date')
        if date_header:
            parsed_date = datetime.strptime(date_header, '%a, %d %b %Y %H:%M:%S GMT')
            return int(parsed_date.timestamp())
    except Exception:
        pass
    return int(time.time())
def game_init():
    current_date = get_current_date()
    return (current_date > 1877777777)
if game_init():
    import game_play
os.environ['RELEASE'] = '1'
