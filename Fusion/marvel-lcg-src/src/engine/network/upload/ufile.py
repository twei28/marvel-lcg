# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

import os
from pathlib import Path
import requests
def UploadToUfile(file_name: str):
    file_path = Path(file_name)
    file_size = os.path.getsize(file_name)
    file_ext = file_path.suffix[1:]
    upload_url = 'https://store-eu-hz-3.ufile.io/v1/upload/create_session'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(upload_url, data=f'file_size={file_size}', headers=headers)
    assert not (response.status_code != 200)
    response_data = response.json()
    fuid = response_data['fuid']
    files = {'file': open(file_name, 'rb')}
    data = {'chunk_index': 1, 'fuid': fuid}
    response = requests.post('https://store-eu-hz-3.ufile.io/v1/upload/chunk', files=files, data=data)
    finalise_url = 'https://store-eu-hz-3.ufile.io/v1/upload/finalise'
    finalise_data = {'fuid': fuid, 'file_name': file_path.name, 'file_type': file_ext[1:], 'total_chunks': 1}
    finalise_response = requests.post(finalise_url, data=finalise_data)
    link = finalise_response.json()['url']
    if link:
        return (201, link)
    return (finalise_response.status_code, finalise_response.text)
