from core import *
import requests
from engine.lib import ImageCreator, ImageLib
from engine.log import Log
from engine.file import FileManager
from engine.config import ConfigVariables

CATEGORY_NAME = "CACHE"

IMAGE_FOLDERS   = ConfigVariables.Folders('image_folders', ["./assets/pics/", "./assets/pics-fr/"])
# Les vignettes : les memes scans, reduits sur le serveur au petit cote de 246
# px, avec un vrai filtre de reduction et un masque flou. C'est ce que le
# plateau affiche ; le scan complet reste pour l'apercu agrandi. Voir
# tools/generer_vignettes.py pour le pourquoi (08/09/2026).
VIGNETTE_FOLDER = ConfigVariables.Folder('vignette_folder', "./assets/vignettes/")
# Les scans HAUTE DEFINITION (715 px) des cartes officielles, pour la scene de
# l'assistant qui etire l'image du heros ou du mechant sur un panneau de plus
# de 1 000 px : le scan anglais local n'y fait que 300 px (08/09/2026,
# « augmenter la resolution de l'image a la selection »). Telecharges a la
# demande depuis les serveurs d'images deja configures (image_servers), et
# gardes ici pour toujours. Voir aussi tools/telecharger_scans_hd.py.
HD_FOLDER = ConfigVariables.Folder('hd_folder', "./assets/pics-hd/")
TEXTURE_FOLDER  = ConfigVariables.Folder('texture_folder', "./assets/textures/")
CACHE_FOLDER    = ConfigVariables.Folder('cache_folder', "./assets/cache/")
IMAGE_SERVERS   = ConfigVariables.ListStr('image_servers', [])
SAVE_EMPTY_IMAGE = ConfigVariables.Bool('save_empty_image', True)
BREAK_WHEN_LOAD_ONLINE_IMAGE = ConfigVariables.Bool('break_when_load_online_image', False)

class Cache:

    cache: Dict[str, bytes] = {}
    link_pic: Dict[str, str] = {}

    @staticmethod
    def SetLinkPic(card_id: str, link_to_pic_id: str):
        Cache.link_pic[card_id] = link_to_pic_id

    @staticmethod
    def SetCache(card_id: str, data: bytes):
        Cache.cache[card_id] = data

    @staticmethod
    def LoadImageHD(card_id: str) -> bytes:
        """Le scan haute definition d'une carte officielle, ou le scan habituel.

        Ordre : le fichier deja telecharge dans HD_FOLDER ; sinon, pour un
        identifiant officiel, un telechargement depuis image_servers, garde
        dans HD_FOLDER ; sinon (fan-made, hors ligne, serveur muet) le scan
        habituel. Le navigateur ne voit jamais d'echec."""
        card_id = card_id.lstrip("/")
        cle = "hd:" + card_id
        if cle in Cache.cache:
            return Cache.cache[cle]
        for ext_name in [".jpg", ".webp", ".png"]:
            check_path = f"{HD_FOLDER.value}/{card_id}{ext_name}"
            if FileManager.Exists(check_path):
                with FileManager.OpenFile(check_path, read=True, bin=True) as file:
                    data = ImageLib.TryRotateImage(file.Read())
                Cache.cache[cle] = data
                return data
        data = Cache.TelechargerHD(card_id)
        if data:
            Cache.cache[cle] = data
            return data
        return Cache.LoadImage(card_id)

    @staticmethod
    def TelechargerHD(card_id: str) -> bytes | None:
        """Telecharge le scan HD d'un identifiant OFFICIEL et le garde dans
        HD_FOLDER. Rend None pour tout le reste (fan-made, echec, hors ligne).
        Meme liste de serveurs et memes en-tetes que LoadImage."""
        import re
        if not IMAGE_SERVERS.value or not re.match(r'^\d{5}[a-z]?$', card_id):
            return None
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        for site in IMAGE_SERVERS.value:
            full_url = site.replace('{card_id}', card_id).replace('{card_id:U}', card_id.upper())
            try:
                response = requests.get(full_url, headers=headers, timeout=5)
                response.raise_for_status()
                if 'image/' not in (response.headers.get('Content-Type') or ''):
                    continue
                data = response.content
                # Un serveur qui ne rend qu'une petite image (marvelcdb : 300 px)
                # n'apporte rien : on ne garde que ce qui est vraiment plus grand.
                if len(data) < 60_000:
                    continue
                chemin = FileManager.JoinPath(HD_FOLDER.value, f"{card_id}.jpg")
                FileManager.MakeDir(FileManager.GetDirName(chemin))
                with FileManager.OpenFile(chemin, write=True, bin=True) as file:
                    file.Write(data)
                Log.DebugInfo(CATEGORY_NAME, f"HD telecharge : {card_id} depuis {full_url}")
                return ImageLib.TryRotateImage(data)
            except requests.exceptions.RequestException as e:
                Log.Warn(CATEGORY_NAME, f"HD : {full_url} : {e}")
        return None

    @staticmethod
    def LoadVignette(card_id: str) -> bytes:
        """La vignette d'un scan, ou le scan complet si elle n'existe pas.

        ⚠ LE REPLI EST COTE SERVEUR, ET C'EST VOULU : une carte dont la
        vignette manque (pack ajoute sans relancer l'outil) doit s'afficher
        quand meme, en pleine taille, plutot que tomber sur l'image vide. Le
        navigateur ne voit jamais la difference."""
        card_id = card_id.lstrip("/")
        cle = "vignette:" + card_id
        if cle in Cache.cache:
            return Cache.cache[cle]
        for ext_name in [".jpg", ".webp", ".png"]:
            check_path = f"{VIGNETTE_FOLDER.value}/{card_id}{ext_name}"
            if FileManager.Exists(check_path):
                with FileManager.OpenFile(check_path, read=True, bin=True) as file:
                    data = ImageLib.TryRotateImage(file.Read())
                Cache.cache[cle] = data
                return data
        # Une image liee (dos commun, carte renvoyant a une autre) a sa
        # vignette sous le nom de la cible.
        if card_id in Cache.link_pic:
            return Cache.LoadVignette(Cache.link_pic[card_id])
        return Cache.LoadImage(card_id)

    @staticmethod
    def LoadImage(card_id: str) -> bytes:
        # if url in ['enthralled_minion', 'minion', 'ultron_facedown_drone']:
        #     url = 'player'
        card_id = card_id.lstrip("/")

        if card_id in Cache.cache:
            return Cache.cache[card_id]

        assert card_id != "", f"{card_id=}"
        file_name = card_id

        check_folders = IMAGE_FOLDERS.value + [TEXTURE_FOLDER.value] + [CACHE_FOLDER.value]

        def try_load_image_data(image_data: bytes):
            return ImageLib.TryRotateImage(image_data)

        # Load the image from the cache and images
        def try_load_image_path(file_path: str) -> bytes|None:
            for ext_name in [".webp", ".jpg", ".png"]:
                check_path = file_path + ext_name
                if FileManager.Exists(check_path):
                    with FileManager.OpenFile(check_path, read=True, bin=True) as file:
                        return try_load_image_data(file.Read())
            return None

        def try_load_image_name(name: str) -> bytes|None:
            for cache_folder in check_folders:
                file_paths: List[str] = []
                file_paths.append(f"{cache_folder}/{name}")
                for file_path in file_paths:
                    image_data = try_load_image_path(file_path)
                    if image_data:
                        return image_data
            return None

        image_data = try_load_image_name(file_name)
        if image_data:
            Cache.SetCache(file_name, image_data)
            return image_data

        if file_name in Cache.link_pic:
            image_data = Cache.LoadImage(Cache.link_pic[file_name])
            if image_data:
                return image_data

        # Repli "fr_" vers l'anglais. La liste scans-fr-liste.ts est versionnee
        # dans git, mais les 456 Mo d'images de assets/pics-fr/ ne le sont pas :
        # toute copie du depot, toute reinstallation du moteur, se retrouve avec
        # une liste pleine et zero image. Sans ce repli, chaque carte "fr_xxxxx"
        # tomberait en silence sur le telechargement en ligne ou sur une image
        # vide generee, alors que le scan anglais est deja present sur le
        # disque. On retente donc avec le nom prive du prefixe avant toute
        # autre strategie de secours, ce qui rend le systeme sur meme sur une
        # installation ou le pack FR n'a jamais ete importe.
        if file_name.startswith("fr_"):
            image_data = Cache.LoadImage(file_name[len("fr_"):])
            if image_data:
                Cache.SetCache(file_name, image_data)
                return image_data

        def check_is_card_id(s: str):
            import re
            # Pattern to match: four digits followed by a lowercase letter
            pattern = r'^\d{5}[a-z]?$'
            return re.match(pattern, s)

        def save_to_file(file_name: str, ext_name: str, data: bytes):
            file_path = FileManager.JoinPath(CACHE_FOLDER.value, f"{file_name}.{ext_name}")
            FileManager.MakeDir(FileManager.GetDirName(file_path))
            with FileManager.OpenFile(file_path, write=True, bin=True) as file:
                file.Write(data)

        is_time_out = True
        if IMAGE_SERVERS.value and check_is_card_id(card_id):
            # Load the image from the internet
            skip_break = not BREAK_WHEN_LOAD_ONLINE_IMAGE.value
            if not skip_break:
                Debug.DebugBreak()

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # "https://cerebrodatastorage.blob.core.windows.net/cerebro-cards/official/${card_id}.jpg",
            # "https://marvelcdb.com/bundles/cards/${card_id}.jpg",
            # "https://marvelcdb.com/bundles/cards/${card_id}.png",

            is_time_out = False

            for site in IMAGE_SERVERS.value:
                full_url = site
                full_url = full_url.replace('{card_id}', card_id)
                full_url = full_url.replace('{card_id:U}', card_id.upper())

                try:
                    Log.DebugInfo(CATEGORY_NAME, f"Downloading from {full_url}")

                    response = requests.get(full_url, headers=headers, timeout=3)
                    response.raise_for_status()

                    content_type = response.headers.get('Content-Type')

                    ext_name = "bmp"
                    if content_type:
                        # Determine the image format based on the Content-Type
                        if 'image/jpeg' in content_type:
                            ext_name = "jpg"
                        elif 'image/png' in content_type:
                            ext_name = "png"
                        elif 'image/webp' in content_type:
                            ext_name = "webp"

                    # Check if the response is successful
                    Log.DebugInfo(CATEGORY_NAME, f"Downloaded: {file_name}")
                    data = response.content
                    # Save the image to the cache
                    save_to_file(file_name, ext_name, data)
                    # Get the image data from the response
                    image_data = try_load_image_data(data)
                    Cache.SetCache(file_name, image_data)
                    return image_data
                except requests.exceptions.Timeout:
                    Log.Warn(CATEGORY_NAME, f"Timeout occurred while downloading {file_name}")
                    is_time_out = True
                except requests.exceptions.RequestException as e:
                    Log.Warn(CATEGORY_NAME, f"Request failed with error: {e}")

        # raise Exception(f"Failed to load {file_name} from the internet")
        image_data = ImageCreator.CreateNoImage(card_id)
        if SAVE_EMPTY_IMAGE.value and not is_time_out:
            save_to_file(file_name, "jpg", image_data)
        Cache.SetCache(file_name, image_data)
        return image_data

