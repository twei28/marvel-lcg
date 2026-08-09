# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

import requests
def UploadToPastebin(api_dev_key: str, api_user_key: str, file_content: str, paste_title: str, paste_expiration: str = 'N'):
    data = {'api_dev_key': api_dev_key, 'api_option': 'paste', 'api_paste_code': file_content, 'api_user_key': api_user_key, 'api_paste_name': paste_title, 'api_paste_expire_date': paste_expiration, 'api_paste_format': 'json'}
    response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    if (response.status_code == 200):
        return (201, response.text)
    return (response.status_code, response.text)
