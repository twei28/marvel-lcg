# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

from core import *
import requests
def UploadToGist(api_token: str, file_content: str, filename: str, description: str = '', is_public: bool = True) -> Tuple[(int, str)]:
    headers = {'Authorization': f'Bearer {api_token}', 'Accept': 'application/vnd.github.v3+json'}
    data = {'description': description, 'public': is_public, 'files': {filename: {'content': file_content}}}
    response = requests.post('https://api.github.com/gists', headers=headers, json=data)
    if (response.status_code == 201):
        return (201, response.json()['html_url'])
    return (response.status_code, response.text)
