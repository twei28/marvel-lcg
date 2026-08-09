# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

from core import *
import requests
from engine.config import ConfigVariables
CLOUDFLARE_WORKER_ADDRESS = ConfigVariables.Str('cloudflare_worker_address', 'https://marvel-lcg-reports.irefrixs.workers.dev/')
def UploadToCloudflare(file_content: str, filename: str, description: str = '', is_public: bool = True) -> Tuple[(int, str)]:
    data = {'description': description, 'public': is_public, 'files': {filename: {'content': file_content}}}
    response = requests.post(CLOUDFLARE_WORKER_ADDRESS.value, json=data)
    if (response.status_code == 201):
        return (201, list(response.json()['files'].keys())[0])
    return (response.status_code, response.text)
