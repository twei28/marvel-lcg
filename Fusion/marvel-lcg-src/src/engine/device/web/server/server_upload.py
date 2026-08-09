# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

from core import *
from core.lib import Time
from aiohttp import web
from build import Build
from engine.device.web.server.server_base import GameServerBase
from engine.log import Log
from engine.network.upload.ufile import UploadToUfile
from engine.network.upload.pastebin import UploadToPastebin
from engine.network.upload.gist import UploadToGist
from engine.network.upload.cloudflare import UploadToCloudflare
from engine.user.user_info import UserInfo
from engine.config import ConfigVariables
PASTEBIN_API_DEV_KEY = ConfigVariables.Str('pastebin_api_dev_key', '')
PASTEBIN_API_USER_KEY = ConfigVariables.Str('pastebin_api_user_key', '')
GITHUB_GIST_TOKEN = ConfigVariables.Str('github_gist_token', '')
CATEGORY_NAME = 'UPLOAD'
class GameServerUpload(GameServerBase):
    def start_uploading(self) -> bool:
        from cards.database import CardsDB
        ok = (CardsDB.checksum_ok and (Build.release and (not CardsDB.cards_custom_files)))
        if ok:
            Log.Info(CATEGORY_NAME, 'Uploading, please wait')
        return ok
    def process_upload_result(self, status_code: int, result: str, server: str):
        if not (Build.release):
            Log.Info(CATEGORY_NAME, f'Server: {server}')
        if (200 <= status_code < 300):
            Log.Info(CATEGORY_NAME, f'Uploaded: {result}')
        else:
            Log.Assert(CATEGORY_NAME, f'Upload failed: {result}')
        if (status_code == 201):
            self.uploaded_file_names.add(result)
        if (200 <= status_code < 300):
            return web.Response(text=result)
        return web.Response(status=400, text=result)
    def upload_to_ufile(self, request: web.Request) -> web.Response:
        scene_name = f'./{self.game.scene.GetSaveFileName(False)}.json'
        self.game.session.SaveScene(scene_name, delete_old=False)
        status_code, result = UploadToUfile(scene_name)
        return self.process_upload_result(status_code, result, 'ufile.io')
    def upload_to_pastebin(self, request: web.Request) -> web.Response:
        data = self.game.session.DumpSave()
        api_dev_key = PASTEBIN_API_DEV_KEY.value
        api_user_key = PASTEBIN_API_USER_KEY.value
        file_name = f'{self.game.scene.GetSaveFileName(False)}.json'
        status_code, result = UploadToPastebin(api_dev_key, api_user_key, data, file_name)
        return self.process_upload_result(status_code, result, 'pastebin.com')
    def upload_to_gist(self, request: web.Request) -> web.Response:
        data = self.game.session.DumpSave()
        api_token = GITHUB_GIST_TOKEN.value
        file_name = f'{self.game.scene.GetSaveFileName(False)}.json'
        description = UserInfo.text
        status_code, result = UploadToGist(api_token, data, file_name, description)
        return self.process_upload_result(status_code, result, 'github.com')
    def upload_to_cloudflare(self, request: web.Request) -> web.Response:
        if not (self.start_uploading()):
            return self.process_upload_result(400, 'Upload initiation failed.', 'cloudflare.com')
        report = request.rel_url.query.get('r', '')
        upload_type = request.rel_url.query.get('t', '')
        client_info = self.device_manager.client_manager.GetInfo()
        data = self.game.session.DumpSave(report, client_info)
        browser = f"{request.headers.get('User-Agent', 'unknown')}|{request.headers.get('Accept-Language', 'Unknown')}"
        file_name = f'{self.game.scene.GetSaveFileName(False)}.json'
        description = f"{UserInfo.text}|{browser}|{Time.GetElapsedTime():.3f}|{upload_type}"
        status_code = 400
        uploaded_name = 'Server error.'
        try:
            if (file_name in self.uploaded_file_names):
                status_code, uploaded_name = 200, file_name
                Log.Warn(CATEGORY_NAME, 'This file has already been uploaded')
            else:
                status_code, uploaded_name = UploadToCloudflare(data, file_name, description, False)
        finally:
            return self.process_upload_result(status_code, uploaded_name, 'cloudflare.com')
    def test_job_block_thread(self, request: web.Request) -> web.Response:
        import time
        time.sleep(10)
        return web.Response(text='Done')
    async def save_local(self, request: web.Request) -> web.Response:
        result = self.game.session.SaveScene(delete_old=False)
        return web.Response(text=result)
    @override
    def __init__(self) -> None:
        super().__init__()
        self.uploaded_file_names = set()
        self.AddNonAwaitGetSecurity('/upload_cloudflare', self.upload_to_cloudflare)
        self.AddAwaitGetSecurity('/save_local', self.save_local)
        self.AddNonAwaitGetSecurity('/block_thread', self.test_job_block_thread)
